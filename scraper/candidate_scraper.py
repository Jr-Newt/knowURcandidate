"""
Candidate Scraper — ECI Affidavit Portal
Uses Playwright for headless browser automation.
Implements rate limiting and retry with exponential backoff.
"""

import asyncio
import json
import random
import time
import os
from pathlib import Path
from playwright.async_api import async_playwright

# ─── Config ───
BASE_URL = "https://affidavit.eci.gov.in/"
MAX_RETRIES = 3
BASE_DELAY = 2  # seconds
RATE_LIMIT_DELAY = (2, 4)  # random range in seconds
OUTPUT_DIR = Path(__file__).parent / "output"


async def scrape_with_retry(page, url, retries=MAX_RETRIES):
    """Navigate with exponential backoff retry."""
    for attempt in range(retries):
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            return True
        except Exception as e:
            wait = BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
            print(f"  Retry {attempt + 1}/{retries} after {wait:.1f}s — {e}")
            await asyncio.sleep(wait)
    return False


async def rate_limit():
    """Random delay between requests to avoid detection."""
    delay = random.uniform(*RATE_LIMIT_DELAY)
    await asyncio.sleep(delay)


async def extract_candidate_data(page):
    """
    Extract candidate information from the current affidavit page.
    Returns a dict with all required fields.
    """
    # NOTE: Selectors below are illustrative. The actual selectors will depend
    # on the ECI portal's DOM structure and may need adjustment.
    data = {}
    try:
        data["name"] = await page.text_content(".candidate-name") or ""
        data["party"] = await page.text_content(".party-name") or ""
        data["constituency"] = await page.text_content(".constituency-name") or ""
        data["education"] = await page.text_content(".education") or ""
        data["profession"] = await page.text_content(".profession") or ""
        data["age"] = await page.text_content(".age") or ""

        # Criminal cases
        data["criminal_cases"] = 0
        data["serious_cases"] = 0
        criminal_el = await page.query_selector(".criminal-cases")
        if criminal_el:
            text = await criminal_el.text_content()
            data["criminal_cases"] = int(text) if text.isdigit() else 0

        # Assets and liabilities
        data["assets"] = 0
        data["liabilities"] = 0
        assets_el = await page.query_selector(".total-assets")
        if assets_el:
            text = (await assets_el.text_content()).replace(",", "").strip()
            data["assets"] = int(text) if text.isdigit() else 0

        liabilities_el = await page.query_selector(".total-liabilities")
        if liabilities_el:
            text = (await liabilities_el.text_content()).replace(",", "").strip()
            data["liabilities"] = int(text) if text.isdigit() else 0

        data["affidavit_link"] = page.url

    except Exception as e:
        print(f"  Error extracting data: {e}")

    return data


async def scrape_candidates(state="Kerala", election_type="Assembly"):
    """
    Main scraper flow:
    1. Navigate to ECI portal
    2. Select state and election
    3. Iterate through constituencies
    4. Extract candidate data
    5. Save as JSON
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_candidates = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"Navigating to {BASE_URL}...")
        success = await scrape_with_retry(page, BASE_URL)
        if not success:
            print("Failed to load ECI portal after retries.")
            await browser.close()
            return []

        # NOTE: The actual scraping logic depends on the ECI portal's structure.
        # Below is a framework that should be adapted to the real DOM.
        # ─────────────────────────────────────────────────────────────

        # 1. Select state (Kerala)
        print(f"Selecting state: {state}")
        # await page.select_option("#state-select", label=state)
        # await rate_limit()

        # 2. Select election type
        # await page.select_option("#election-type", label=election_type)
        # await rate_limit()

        # 3. Get list of constituencies
        # constituency_links = await page.query_selector_all(".constituency-link")

        # 4. For each constituency, get candidates
        # for link in constituency_links:
        #     await link.click()
        #     await rate_limit()
        #     candidate_els = await page.query_selector_all(".candidate-row")
        #     for candidate_el in candidate_els:
        #         await candidate_el.click()
        #         await rate_limit()
        #         data = await extract_candidate_data(page)
        #         if data.get("name"):
        #             all_candidates.append(data)
        #         await page.go_back()
        #         await rate_limit()

        await browser.close()

    # Save raw output
    output_file = OUTPUT_DIR / "candidates_raw.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(all_candidates)} candidates → {output_file}")
    return all_candidates


if __name__ == "__main__":
    asyncio.run(scrape_candidates())
