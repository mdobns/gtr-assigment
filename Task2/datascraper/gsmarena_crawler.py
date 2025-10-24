from bs4 import BeautifulSoup
import requests, time, re

class RateLimitError(Exception):
    """Custom exception for rate limit detection"""
    pass

class PhoneDataCrawler:
    """
    This is for getting data for popular smartphones and their specs
    """
    def __init__(self, html_page):
        self.soup = BeautifulSoup(html_page, 'html.parser')

    def _get_specs(self,spec_name):
        tag = self.soup.find(attrs={'data-spec': spec_name})
        if tag:
            return tag.get_text(strip=True)
        return "Not found"

    def spec_scraper(self):
        phone_data = {}

        phone_data['model_name'] = self._get_specs('modelname')
        phone_data['release_date'] = self._get_specs('released-hl')

        display_size = self._get_specs('displaysize-hl')
        display_type = self._get_specs('displaytype')
        display_resolution = self._get_specs('displayresol-hl')

        phone_data['display'] = f"{display_size}, {display_type}, {display_resolution}"

        phone_data['battery'] = self._get_specs('batdescription1')

        back_camera = self._get_specs('cam1modules')
        front_camera = self._get_specs('cam2modules')
        phone_data['camera'] = f"Main camera {back_camera} \n Front camera {front_camera}"

        phone_data['ram_storage_options'] = self._get_specs('internalmemory')

        match = re.search(r"\$\s*[\d,.]+", self._get_specs('price'))
        if match:
            phone_data['price'] = float(match.group().replace("$", "").replace(",", "").strip())


        return phone_data

class MainScraper:
    BASE_URL = "https://www.gsmarena.com/"

    def __init__(self, headers):
        self.headers = headers

    def fetch_html(self, url, max_retries=3, delay=2):
        last_error = None
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit detected - stopping scraper")
                else:
                    print(f"Error getting data from {url}, Error code {response.status_code}")
                    time.sleep(delay)
            except RateLimitError:
                raise
            except (requests.ConnectionError, requests.Timeout) as e:
                print(f"Connection error on attempt {attempt + 1}: {str(e)}")
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
                # Don't raise connection errors, just return None
                return None
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
                return None
        return None

    def get_phones_urls(self, list_page_url):
        html_doc = self.fetch_html(list_page_url)
        if not html_doc:
            print(f"Failed to fetch HTML from {list_page_url}")
            return []

        soup = BeautifulSoup(html_doc, 'html.parser')
        urls = []
        list_urls = soup.select('div.makers ul li a')
        if not list_urls:
            print("No phone listings found on the page")
            return []
            
        for url in list_urls:
            full_url = self.BASE_URL + url['href']
            urls.append(full_url)
        return urls

    def get_phones_spec(self, list_page_url, limit=0):
        all_phones_data = []
        phones_links = self.get_phones_urls(list_page_url)

        if not phones_links:
            print("No phones links were found")
            return all_phones_data

        # If limit is 0 or greater than available links, use all links
        if limit <= 0 or limit > len(phones_links):
            limit = len(phones_links)

        print(f"Starting to scrape {limit} phones...")
        
        for i, url in enumerate(phones_links[:limit], 1):
            try:
                print(f"Fetching phone {i}/{limit}: {url}")
                phone_page = self.fetch_html(url)
                if not phone_page:
                    print(f"Failed to fetch phone data from {url}")
                    continue
                
                crawl_data = PhoneDataCrawler(phone_page)
                phone_data = crawl_data.spec_scraper()
                all_phones_data.append(phone_data)

                #This helps to get rid of too many attemps from gsmarena
                time.sleep(1)
                    
            except RateLimitError as e:
                print(f"Rate limit hit at phone {i}. Stopping scraper but keeping scraped data.")
                break
            except Exception as e:
                print(f"Error processing phone {url}: {str(e)}")
                continue
                
        print(f"Successfully scraped {len(all_phones_data)} phones out of {limit} attempted")
        return all_phones_data












