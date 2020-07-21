from scrapy import Spider, Request
from howlongtobeat.items import HowlongtobeatItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
search_url = "https://howlongtobeat.com/#search"

class HowLongToBeatSpider(Spider):
    name = 'howlongtobeat_spider'
    allowed_urls = ['https://howlongtobeat.com']
    start_urls = ['https://howlongtobeat.com/game?id=']

    def __init__(self):
        driver = webdriver.Chrome()

    def parse(self, response):
        driver.get(search_url)
        try:
            page_tab_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[@class="search_list_page back_secondary shadow_box"]'))
            )
        except:
            raise Exception('Can\'t find page count.')
        finally:
            # print('='*50)
            # print('Elements Loaded')
            # print('='*50)
            pass

        number_of_pages = int(page_tab_elements[-1].text)

        # print(f'There are {number_of_pages} total pages to scrape.')

        search_url_list = [f'{search_url}{i+1}' for i in range(number_of_pages)]

        for url in search_url_list[:10]:
            for item in self.parse_search_page(url):
                yield item

        driver.close()

    def parse_search_page(self, search_page_url):
        driver.get(search_page_url)
        time.sleep(.5)
        try:
            page_tab_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="search_list_details"]'))
            )
        except:
            raise Exception('Can\'t find game IDs.')
        finally:
            print('='*50)
            print(f'There are {len(page_tab_elements)} games')
            print('='*50)
            pass

        game_urls = [page_tab_element.find_element_by_xpath('.//h3/a').get_property('href') for page_tab_element in page_tab_elements]

        # game_urls = [f'https://howlongtobeat.com/{url}' for url in game_urls]

        # print('='*50)
        # print(f'Start set of URLs')
        # print('='*50)
        # for url in game_urls:
        #     print(url)
        # print('='*50)
        # print(f'End set of URLs')
        # print('='*50)

        for url in game_urls[:10]:
            yield Request(url=url, callback=self.parse_game_page)

    def parse_game_page(self, response):
        game_name = response.xpath('//div[@class="profile_header shadow_text"]/text()').extract_first()  
        # rating = int(review.xpath('.//div[@class="c-ratings-reviews-v2 v-small"]/i/@alt').extract_first())

        # helpful = review.xpath('.//button[@data-track="Helpful"]/text()').extract_first()
        # helpful = int(re.findall('\d+', helpful)[0])

        # unhelpful = review.xpath('.//button[@data-track="Unhelpful"]/text()').extract_first()
        # unhelpful = int(re.findall('\d+', unhelpful)[0])

        item = HowlongtobeatItem()
        item['game_name'] = game_name
        # item['rating'] = rating
        # item['text'] = text
        # item['title'] = title
        # item['helpful'] = helpful
        # item['unhelpful'] = unhelpful
        # item['product'] = response.meta['product']
        # item['model'] = response.meta['model']
        # item['sku'] = response.meta['sku']
        # item['q_and_a'] = response.meta['q_and_a']

        yield item