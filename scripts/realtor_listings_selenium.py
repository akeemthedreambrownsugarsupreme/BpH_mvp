from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class SeleniumScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def start_browser(self):
        # Setup Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)
        time.sleep(5)  # Adjust time as necessary to ensure the page loads completely

    def get_html(self):
        html_content = self.driver.page_source
        return html_content

    def close_browser(self):
        self.driver.quit()

def get_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def fetch_listing_urls_from_html(html_soup, selector_head, selector_tail):
    post_count = 0
    for i in range(1, 13):  # Example: loop through 12 elements
        selector = f"{selector_head}{i}{selector_tail}"
        try:
            job_post_html = html_soup.select(selector)
            if job_post_html:
                job_post_soup = BeautifulSoup(str(job_post_html[0]), 'html.parser')
                job_title = job_post_soup.a.get('title', 'No title found')
                print(job_title)
                post_count += 1
        except Exception as e:
            print(f"Failed to process selector {selector}: {e}")
    return post_count

if __name__ == '__main__':
    url = 'https://www.realtor.ca/ab/edmonton/real-estate'
    scraper = SeleniumScraper(url)
    scraper.start_browser()

    html_content = scraper.get_html()
    soup = get_soup(html_content)

    # Define your CSS selectors as needed
    selector_head = '#SEOCardList > ul > li:nth-child('
    selector_tail = ') > div > a'
    post_count = fetch_listing_urls_from_html(soup, selector_head, selector_tail)
    print("Total Available Job Post in First Page: ", post_count)

    scraper.close_browser()
