"""
News Scraper — Google News & trusted Indian sources
Fetches recent news for each candidate based on name + constituency.
"""

import asyncio
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

import httpx

OUTPUT_DIR = Path(__file__).parent / "output"

# Trusted sources whitelist
TRUSTED_SOURCES = {
    "thehindu.com", "ndtv.com", "indianexpress.com",
    "manoramaonline.com", "mathrubhumi.com", "deccanherald.com",
    "indiatoday.in", "thenewsminute.com", "livelaw.in",
    "onmanorama.com", "news18.com", "hindustantimes.com",
}

MAX_ARTICLES_PER_CANDIDATE = 10
LOOKBACK_MONTHS = 12
RATE_LIMIT_DELAY = (1, 3)


def build_query(name: str, constituency: str) -> str:
    """Build search query for Google News."""
    return f'"{name}" "{constituency}" Kerala election'


def is_trusted(url: str) -> bool:
    """Check if URL belongs to a trusted source."""
    return any(domain in url.lower() for domain in TRUSTED_SOURCES)


def is_recent(date_str: str, months: int = LOOKBACK_MONTHS) -> bool:
    """Check if date is within the lookback window."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        cutoff = datetime.now() - timedelta(days=months * 30)
        return date >= cutoff
    except (ValueError, TypeError):
        return True  # Include if date is unparseable


def deduplicate(articles: list) -> list:
    """Remove duplicate articles by URL."""
    seen = set()
    unique = []
    for a in articles:
        url = a.get("url", "").rstrip("/")
        if url and url not in seen:
            seen.add(url)
            unique.append(a)
    return unique


async def search_news_for_candidate(
    client: httpx.AsyncClient,
    name: str,
    constituency: str,
) -> list:
    """
    Search for news articles about a candidate.

    NOTE: This is a framework. In production, you would use:
    - Google News RSS feed
    - Google Custom Search API
    - Or a news aggregation API

    The actual implementation depends on your API keys and approach.
    """
    query = build_query(name, constituency)
    articles = []

    # Example: Google News RSS feed (no API key needed)
    rss_url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        response = await client.get(rss_url, timeout=15)
        if response.status_code == 200:
            # Parse RSS XML
            from xml.etree import ElementTree
            root = ElementTree.fromstring(response.text)
            channel = root.find("channel")
            if channel:
                for item in channel.findall("item")[:MAX_ARTICLES_PER_CANDIDATE]:
                    title = item.findtext("title", "")
                    link = item.findtext("link", "")
                    pub_date = item.findtext("pubDate", "")
                    source = item.findtext("source", "")

                    # Parse date
                    parsed_date = None
                    if pub_date:
                        try:
                            from email.utils import parsedate_to_datetime
                            dt = parsedate_to_datetime(pub_date)
                            parsed_date = dt.strftime("%Y-%m-%d")
                        except Exception:
                            pass

                    articles.append({
                        "title": title,
                        "url": link,
                        "source": source,
                        "published_date": parsed_date,
                        "summary": None,
                    })

    except Exception as e:
        print(f"  Error fetching news for {name}: {e}")

    # Filter and deduplicate
    articles = [a for a in articles if is_recent(a.get("published_date", ""))]
    articles = deduplicate(articles)

    return articles[:MAX_ARTICLES_PER_CANDIDATE]


async def scrape_news(candidates: list) -> dict:
    """
    Scrape news for a list of candidates.

    Args:
        candidates: List of dicts with 'name' and 'constituency' keys

    Returns:
        Dict mapping candidate name to list of articles
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_news = {}

    async with httpx.AsyncClient() as client:
        for i, c in enumerate(candidates):
            name = c.get("name", "")
            constituency = c.get("constituency", "")
            if not name:
                continue

            print(f"[{i+1}/{len(candidates)}] Fetching news for {name} ({constituency})...")

            articles = await search_news_for_candidate(client, name, constituency)
            all_news[name] = articles

            print(f"  Found {len(articles)} articles")

            # Rate limit
            await asyncio.sleep(random.uniform(*RATE_LIMIT_DELAY))

    # Save output
    output_file = OUTPUT_DIR / "news_raw.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, indent=2, ensure_ascii=False)

    print(f"Total news fetched → {output_file}")
    return all_news


if __name__ == "__main__":
    # Example usage with sample candidates
    sample = [
        {"name": "Shashi Tharoor", "constituency": "Thiruvananthapuram"},
        {"name": "Pinarayi Vijayan", "constituency": "Dharmadam"},
    ]
    asyncio.run(scrape_news(sample))
