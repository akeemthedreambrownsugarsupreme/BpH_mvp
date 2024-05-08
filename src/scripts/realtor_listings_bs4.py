from bs4 import BeautifulSoup
import urllib.request

class HTMLParser:
    
    def __init__(self, url=None):
        self.url = url
    
    def get_html(self):
        html_file = None
        try:
            req = urllib.request.Request(
                self.url,
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            )
            html_file = urllib.request.urlopen(req).read()
        except Exception as e:
            print(f"Error in get_html(): {e}")
        return html_file

    def get_soup(self, html_file):
        html_soup = None
        try:
            html_soup = BeautifulSoup(html_file, 'html.parser')
        except Exception as e:
            print(f"Exception in get_soup(): {e}")
        return html_soup

def fetch_listing_urls_from_html(html_soup, selector_head, selector_tail):
    post_count = 0
    
    try:
        for i in range(1, 13):
            try:
                selector = selector_head + str(i) + selector_tail
                print(selector)
                job_post_html = html_soup.select(selector)
                print(job_post_html)
                job_post_soup = HTMLParser().get_soup(str(job_post_html))
                job_title = job_post_soup.a['title']
                print(job_title)
                post_count +=1
            except:
                pass
    except:
        pass

    return post_count

if __name__ == '__main__':
    url = 'https://www.realtor.ca/ab/edmonton/real-estate'
    html_parser = HTMLParser(url)
    html_file = html_parser.get_html()
    html_soup = html_parser.get_soup(html_file)
    print(html_soup)
    selector_head = '#SEOCardList > ul > li:nth-child('
    selector_tail = ') > div > a'
    post_count = fetch_listing_urls_from_html(html_soup, selector_head, selector_tail)
    print("Total Available Job Post in First Page: ", post_count)