# https://www.geeksforgeeks.org/web-scraping/how-to-scrape-the-web-with-playwright-in-python/
from playwright.sync_api import sync_playwright
from page_scraper import scrap_page
from concurrent.futures import ThreadPoolExecutor, as_completed

def main():
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch(headless=False, channel="chrome")

        page = browser.new_page()
        urls = []
        i = 0
        while True:
            i += 1
            page.goto(f"https://www.iranjib.ir/jax/showarchive.php?p=1&_id={i}")

            tables = page.query_selector_all("table")
            if not tables:
                break

            trs = tables[0].query_selector_all("tr")
            stop = False

            for tr in trs:
                tds = tr.query_selector_all('td')
                if not tds:
                    continue

                date = tds[-1].inner_text().strip()

                if 'دی' in date:
                    stop = True
                    break

                a = tds[0].query_selector('a')
                if not a:
                    continue

                title = a.inner_text().strip()
                link = a.get_attribute('href')

                if 'طلا' in title or 'دلار' in title:
                    urls.append(link)

            print("Still looping, i =", i)
            if stop:
                break
            
        page.wait_for_timeout(5000)
        browser.close()
    return urls

def scrape_multithreaded(urls, workers=5):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(scrap_page, url) for url in urls]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    urls = main()
    print("Total URLs:", len(urls))

    scrape_multithreaded(urls, workers=5)
