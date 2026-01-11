import asyncio, hashlib, uuid, re
from datetime import datetime, timezone
import pandas as pd
from playwright.async_api import async_playwright

EVENTS_PER_SITE = 30
CITY = "Sydney"
OUTPUT_FILE = "sydney_events.csv"

SITES = [
    {"name": "sydney.com", "url": "https://www.sydney.com/events", "link_hint": "/event"},
    {"name": "eventbrite", "url": "https://www.eventbrite.com/d/australia--sydney/events/", "link_hint": "/e/"},
    {"name": "cityofsydney", "url": "https://whatson.cityofsydney.nsw.gov.au/", "link_hint": "/events/"}
]

# ---------------- LANGUAGE FILTERS ---------------- #

BAD_TITLES = [
    "what's on in sydney",
    "was ist los in sydney",
    "悉尼",
    "シドニー",
    "시드니"
]

def is_bad_title(title: str) -> bool:
    return any(bad in title.lower() for bad in BAD_TITLES)

def is_english_title(title: str) -> bool:
    if not title:
        return False
    if re.search(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]', title):
        return False
    if not re.search(r'[A-Za-z]', title):
        return False
    return len(re.findall(r'[A-Za-z]{2,}', title)) >= 2

# ---------------- HELPERS ---------------- #

def make_hash(title, date_text, venue, source):
    return hashlib.sha256(
        f"{title}|{date_text}|{venue}|{source}".encode()
    ).hexdigest()

async def safe_text(page, sel):
    el = await page.query_selector(sel)
    return (await el.text_content()).strip() if el else None

async def safe_attr(page, sel, attr):
    el = await page.query_selector(sel)
    return await el.get_attribute(attr) if el else None

# ---------------- SCRAPER ---------------- #

async def scrape_site(browser, site, seen_hashes):
    page = await browser.new_page()
    await page.goto(site["url"], timeout=60000)
    await page.wait_for_timeout(2000)

    links = []
    for a in await page.query_selector_all("a"):
        href = await a.get_attribute("href")
        if href and site["link_hint"] in href:
            if href.startswith("/"):
                href = site["url"].split("/")[0] + "//" + site["url"].split("/")[2] + href
            if href not in links:
                links.append(href)
        if len(links) >= EVENTS_PER_SITE:
            break

    results = []

    for url in links:
        ev = await browser.new_page()
        try:
            await ev.goto(url, timeout=60000)
            await ev.wait_for_timeout(1200)

            title = await safe_text(ev, "h1")
            if not title:
                await ev.close()
                continue

            if not is_english_title(title) or is_bad_title(title):
                await ev.close()
                continue

            image = (
                await safe_attr(ev, "meta[property='og:image']", "content")
                or await safe_attr(ev, "meta[name='twitter:image']", "content")
            )
            if not image:
                await ev.close()
                continue

            # 🔥 RAW DATE STRING (NO PARSING)
            date_text = (
                await safe_text(ev, "time")
                or await safe_text(ev, "[class*=date]")
                or await safe_text(ev, "[class*=when]")
            )

            venue = (
                await safe_text(ev, "[class*=venue]")
                or await safe_text(ev, "[class*=location]")
            )

            event_hash = make_hash(title, date_text, venue, site["name"])
            if event_hash in seen_hashes:
                await ev.close()
                continue
            seen_hashes.add(event_hash)

            results.append({
                "id": uuid.uuid4().hex,
                "title": title,
                "description": await safe_attr(ev, "meta[name='description']", "content"),
                "image_url": image,
                "start_datetime": date_text,   # ✅ STRING AS-IS
                "end_datetime": None,
                "venue": venue,
                "city": CITY,
                "category": None,
                "ticket_url": url,
                "source": site["name"],
                "source_event_id": None,
                "hash": event_hash,
                "last_seen_at": datetime.now(timezone.utc).isoformat(),
                "created_at": datetime.now(timezone.utc).isoformat()
            })

            print("✔", title, "|", date_text)

        except Exception:
            pass

        await ev.close()

    await page.close()
    return results

# ---------------- MAIN ---------------- #

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        seen_hashes = set()
        all_events = []

        for site in SITES:
            all_events += await scrape_site(browser, site, seen_hashes)

        df = pd.DataFrame(all_events)

        # ❌ NO DATETIME PARSING ANYMORE
        df.to_csv(OUTPUT_FILE, index=False)

        print(f"\nDONE — {len(df)} events saved")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
