from scrapy import Spider, Request
from howlongtobeat.items import HowlongtobeatItem
import csv

class HowLongToBeatSpider(Spider):
    name = 'howlongtobeat_spider'
    allowed_urls = ['https://howlongtobeat.com']
    start_urls = ['https://howlongtobeat.com/game?id=']

    def parse(self, response):
        with open('game_links.csv', newline='') as f:
            reader = csv.reader(f)
            game_links = list(reader)

        for game_link in game_links:
            yield Request(url=game_link[0], callback=self.parse_game_page)

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
