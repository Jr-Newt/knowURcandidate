"""
ECI Affidavit Portal Scraper — 2026 Kerala Assembly Elections
Uses Playwright browser automation to bypass anti-bot protection.

Flow:
1. Launch headless browser → navigate to affidavit portal
2. Select Kerala in the state dropdown → click Filter
3. Parse the loaded HTML for candidate cards
4. Visit each candidate's profile page for detailed info
5. Save all data as JSON
"""

import asyncio
import json
import re
import random
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = "https://affidavit.eci.gov.in"
OUTPUT_DIR = Path(__file__).parent / "output"
RATE_LIMIT = (0.3, 0.7)  # Reduced wait time to speed up 3500+ requests


def parse_number(text: str) -> int:
    """Parse a number string like '1,23,45,678' or 'Rs 12345' into int."""
    if not text:
        return 0
    cleaned = re.sub(r"[^\d]", "", text)
    return int(cleaned) if cleaned else 0


async def scrape_kerala_2026():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_candidates = []

    async with async_playwright() as p:
        # Launch headed to lower bot score, and disable automation flags
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        page = await context.new_page()

        # Inject stealth scripts to hide webdriver
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        # ── Step 1: Navigate to the portal ────────────────────────────
        print("1. Loading ECI affidavit portal...")
        
        try:
            await page.goto(f"{BASE_URL}/candidate-affidavit", wait_until="domcontentloaded", timeout=60000)
            
            # Wait for any prominent element to ensure JS has initialized
            await page.wait_for_selector(".candidate-affidavit-blk, #states, form", timeout=15000)
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Error loading portal: {e}")
            await page.screenshot(path=OUTPUT_DIR / "error_load.png", full_page=True)
            print("Saved screenshot to error_load.png")
            await browser.close()
            return []

        # ── Step 2: Select Kerala and filter ──────────────────────────
        print("2. Selecting Kerala...")
        try:
            # Wait specifically for the states dropdown to be visible and interactive
            await page.wait_for_selector("#states", state="visible", timeout=10000)
        except Exception as e:
            print(f"States dropdown not found: {e}")
            await page.screenshot(path=OUTPUT_DIR / "error_states.png", full_page=True)
            await browser.close()
            return []
            
        # In Playwright, sometimes standard select_option fails on custom dropdowns
        # Let's try standard select first, fallback to JS if needed
        try:
            await page.select_option("#states", label="Kerala")
        except Exception as e:
            print(f"Standard select failed ({e}), trying JavaScript fallback...")
            await page.evaluate("""
                const s = document.querySelector('#states');
                for (let i = 0; i < s.options.length; i++) {
                    if (s.options[i].text.includes('Kerala')) {
                        s.selectedIndex = i;
                        s.dispatchEvent(new Event('change'));
                        break;
                    }
                }
            """)
            
        await page.wait_for_timeout(2000)

        print("3. Clicking Filter...")
        await page.wait_for_selector("button.search.btn-primary", state="visible")
        # Use Force click in case of overlays
        await page.click("button.search.btn-primary", force=True)
        
        print("   Waiting for results to load...")
        # Wait for either the candidate cards container or a no-data message
        try:
            await page.wait_for_selector(".candidate-info", timeout=15000)
        except Exception:
            print("   (Warning: candidate-info class not found quickly, proceeding anyway)")
            
        await page.wait_for_timeout(5000)  # Wait for full results to render
        await page.wait_for_load_state("networkidle")

        # ── Step 3: Loop through pagination and parse all candidates ───────
        print("4. Parsing candidate list across all pages...")
        candidates_basic = []
        page_num = 1
        
        from bs4 import BeautifulSoup
        
        while True:
            print(f"   Parsing page {page_num}...")
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            # Find all "View more" links which point to profile pages
            view_more_links = soup.find_all("a", href=re.compile(r"show-profile"))
            print(f"   Found {len(view_more_links)} 'View more' links on page {page_num}")

            # Extract basic info from each candidate card
            for link in view_more_links:
                href = link.get("href", "")
                if not href.startswith("http"):
                    href = BASE_URL + ("" if href.startswith("/") else "/") + href

                # Walk up the DOM to find the card container
                container = link
                for _ in range(10):
                    container = container.parent
                    if container is None:
                        break
                    text = container.get_text(" ", strip=True)
                    if "Party" in text and "Constituency" in text:
                        break

                card_text = container.get_text(" ", strip=True) if container else ""
                info = {"profile_url": href}

                # Extract from card text
                if container:
                    for tag in container.find_all(["h4", "h5", "h6", "strong"]):
                        t = tag.get_text(strip=True)
                        if t and len(t) > 2 and "Party" not in t and "View" not in t:
                            info["name"] = t
                            break

                party_m = re.search(r"Party\s*:\s*(.+?)(?:\s*(?:Status|State|Constit)\b)", card_text)
                if party_m:
                    info["party"] = party_m.group(1).strip()

                status_m = re.search(r"Status\s*:\s*(\w+)", card_text)
                if status_m:
                    info["status"] = status_m.group(1).strip()

                const_m = re.search(r"Constituency\s*:\s*(.+?)(?:\s*(?:Party|Status|State|View)\b|$)", card_text)
                if const_m:
                    info["constituency"] = const_m.group(1).strip()

                candidates_basic.append(info)
                
            # Try to click the "Next" button
            try:
                # ECI uses tailwind pagination: Next »
                # It might have rel="next" or literal text "Next"
                next_btns = page.locator("a:has-text('Next')")
                count = await next_btns.count()
                
                clicked = False
                for i in range(count):
                    try:
                        btn = next_btns.nth(i)
                        href = await btn.get_attribute("href")
                        if btn and await btn.is_visible() and href and "page=" in href:
                            print("   Clicking Next page...")
                            await btn.click(force=True)
                            await page.wait_for_timeout(4000)
                            await page.wait_for_load_state("networkidle")
                            page_num += 1
                            clicked = True
                            break
                    except:
                        pass
                
                if not clicked:
                    # Alternative JS fallback
                    next_url = await page.evaluate("document.querySelector('a[rel=\"next\"]')?.href || document.evaluate('//a[contains(text(),\"Next\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue?.href")
                    if next_url:
                        print(f"   Navigating via JS to: {next_url}")
                        await page.goto(next_url, wait_until="networkidle", timeout=30000)
                        await page.wait_for_timeout(3000)
                        page_num += 1
                    else:
                        print(f"   End of pagination reached at page {page_num}.")
                        break
            except Exception as e:
                print(f"   Pagination stopped: {e}")
                break

        print(f"\n   Extracted basic info for a total of {len(candidates_basic)} candidate listings")

        # Filter to only "Contesting" candidates (skip Withdrawn/Rejected)
        contesting = [c for c in candidates_basic if c.get("status", "").lower() in ("accepted", "contesting", "")]
        print(f"   Contesting/Accepted candidates: {len(contesting)}")

        # ── Step 4: Visit each candidate's profile for details (Concurrent) ────────
        print(f"\n5. Fetching detailed profiles concurrently for {len(contesting)} candidates...")
        
        # Deduplicate candidates using profile_url
        unique_contesting = {}
        for c in contesting:
            if c["profile_url"] not in unique_contesting:
                unique_contesting[c["profile_url"]] = c
        contesting = list(unique_contesting.values())
        print(f"   Unique candidates to fetch: {len(contesting)}")

        semaphore = asyncio.Semaphore(5)  # 5 concurrent requests
        state = {"completed_count": 0}

        async def fetch_profile(candidate, context):
            url = candidate.get("profile_url", "")
            if not url:
                return candidate

            async with semaphore:
                try:
                    # Create a new page for concurrent fetching
                    p = await context.new_page()
                    # Stealth
                    await p.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
                    
                    await p.goto(url, wait_until="domcontentloaded", timeout=45000)
                    profile_html = await p.content()
                    await p.close()

                    from bs4 import BeautifulSoup
                    profile_soup = BeautifulSoup(profile_html, "html.parser")
                    profile_text = profile_soup.get_text(" ", strip=True)

                    details = {}
                    import json
                    
                    age_m = re.search(r"Age\s*[:]\s*(\d+)", profile_text, re.IGNORECASE)
                    if age_m: details["age"] = int(age_m.group(1))

                    edu_m = re.search(r"Education\s*[:]\s*(.+?)(?:\s*(?:Profession|Self|Criminal|Total|Address)\b)", profile_text, re.IGNORECASE)
                    if edu_m: details["education"] = edu_m.group(1).strip()

                    prof_m = re.search(r"(?:Self\s*)?Profession\s*[:]\s*(.+?)(?:\s*(?:Criminal|Total|Education|Address|Age)\b)", profile_text, re.IGNORECASE)
                    if prof_m: details["profession"] = prof_m.group(1).strip()

                    crim_m = re.search(r"Criminal\s*Cases?\s*[:]\s*(\d+)", profile_text, re.IGNORECASE)
                    if crim_m: details["criminal_cases"] = int(crim_m.group(1))
                    elif re.search(r"no\s*criminal", profile_text, re.IGNORECASE): details["criminal_cases"] = 0

                    serious_m = re.search(r"Serious\s*(?:Criminal\s*)?Cases?\s*[:]\s*(\d+)", profile_text, re.IGNORECASE)
                    if serious_m: details["serious_cases"] = int(serious_m.group(1))

                    assets_m = re.search(r"Total\s*Assets?\s*[:]\s*(?:Rs\.?\s*)?([0-9,]+)", profile_text, re.IGNORECASE)
                    if assets_m: details["assets"] = parse_number(assets_m.group(1))

                    liab_m = re.search(r"Total\s*Liabilit(?:y|ies)\s*[:]\s*(?:Rs\.?\s*)?([0-9,]+)", profile_text, re.IGNORECASE)
                    if liab_m: details["liabilities"] = parse_number(liab_m.group(1))

                    gender_m = re.search(r"Gender\s*[:]\s*(\w+)", profile_text, re.IGNORECASE)
                    if gender_m: details["gender"] = gender_m.group(1).strip()

                    candidate.update(details)
                    candidate["affidavit_link"] = url
                    
                    state["completed_count"] += 1
                    if state["completed_count"] % 100 == 0:
                        print(f"   ✓ {state['completed_count']}/{len(contesting)} profiles fetched...")
                        
                except Exception as e:
                    print(f"✗ Failed {candidate.get('name')}: {e}")
            
            return candidate

        # Run concurrent fetches
        tasks = [fetch_profile(c, context) for c in contesting]
        all_candidates = await asyncio.gather(*tasks)

        # Save progress back out
        with open(OUTPUT_DIR / "candidates_2026_progress.json", "w", encoding="utf-8") as f:
             json.dump(all_candidates, f, indent=2, ensure_ascii=False)
        await browser.close()

    # ── Step 6: Save final output ─────────────────────────────────────
    output_file = OUTPUT_DIR / "candidates_2026_raw.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Scraped {len(all_candidates)} candidates → {output_file}")

    # Print summary
    parties = {}
    for c in all_candidates:
        p = c.get("party", "Unknown")
        parties[p] = parties.get(p, 0) + 1
    print("\nParty breakdown:")
    for party, count in sorted(parties.items(), key=lambda x: -x[1])[:10]:
        print(f"  {party}: {count}")

    print("\n6. Loading data into Supabase...")
    import subprocess
    try:
        subprocess.run(["python", "load_supabase.py"], check=True)
    except Exception as e:
        print(f"Failed to load into Supabase: {e}")

    return all_candidates


if __name__ == "__main__":
    asyncio.run(scrape_kerala_2026())
