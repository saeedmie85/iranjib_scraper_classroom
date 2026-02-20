# https://www.geeksforgeeks.org/web-scraping/how-to-scrape-the-web-with-playwright-in-python/
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch(headless=False, channel="chrome")

        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/")
        all_quotes = page.query_selector_all(".quote")
        for quote in all_quotes:
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            print({"Author": author, "Quote": text})
        page.wait_for_timeout(10000)
        browser.close()


if __name__ == "__main__":
    main()
