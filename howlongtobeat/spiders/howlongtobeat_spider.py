from scrapy import Spider, Request
from howlongtobeat.items import HowlongtobeatItem
import csv
import re

class HowLongToBeatSpider(Spider):
    name = 'howlongtobeat_spider'
    allowed_urls = ['https://howlongtobeat.com']
    start_urls = ['https://howlongtobeat.com/game?id=']

    def parse(self, response):
        # # Small sample file for testing
        # with open('game_links_sample.csv', newline='') as f:
        with open('game_links.csv', newline='') as f:
            reader = csv.reader(f)
            game_links = list(reader)

        # # Limit for testing
        # for game_link in game_links[:200]:
        for game_link in game_links:
            game_id = game_link[0].split('id=')[1]

            meta = {'game_id': game_id}

            yield Request(url=game_link[0], callback=self.parse_game_page, meta=meta)

    def parse_game_page(self, response):
        game_name = response.xpath('//div[@class="profile_header shadow_text"]/text()').extract_first()  
        average_rating = response.xpath('//div[@class="in game_chart back_form shadow_box"]/h5/text()')[0].extract()
        average_rating = float(re.findall('(\d+)% Rating', average_rating)[0])
        rating_count = response.xpath('//div[@class="in game_chart_rev back_form shadow_box"]/h5/text()').extract_first() 
        rating_count = re.findall('Based on (\d*\.*\d+K*) User Ratings*', rating_count)[0]

        rating_count = self.convert_user_count_to_float(rating_count)

        play_times = response.xpath('//table[@class="game_main_table"]/tbody[@class="spreadsheet"]')

        time_to_beat_main_extras = None
        time_to_beat_completionist = None

        for play_time in play_times:
            play_style = play_time.xpath('.//tr/td/text()').extract()
            play_style[1] = self.convert_user_count_to_float(play_style[1])

            if (play_style[0] == 'Main Story'):
                time_to_beat_main_story = self.convert_game_time_to_minutes(play_style[2])
                time_to_beat_main_story_count = play_style[1]
                time_to_beat_main_story_rushed = self.convert_game_time_to_minutes(play_style[4])
                time_to_beat_main_story_leisure = self.convert_game_time_to_minutes(play_style[5])
            elif (play_style[0] == 'Main + Extras'):
                time_to_beat_main_extras = self.convert_game_time_to_minutes(play_style[2])
                time_to_beat_main_extras_count = play_style[1]
                time_to_beat_main_extras_rushed = self.convert_game_time_to_minutes(play_style[4])
                time_to_beat_main_extras_leisure = self.convert_game_time_to_minutes(play_style[5])
            elif (play_style[0] == 'Completionists'):
                time_to_beat_completionist = self.convert_game_time_to_minutes(play_style[2])
                time_to_beat_completionist_count = play_style[1]
                time_to_beat_completionist_rushed = self.convert_game_time_to_minutes(play_style[4])
                time_to_beat_completionist_leisure = self.convert_game_time_to_minutes(play_style[5])

        game_description = None

        game_description = response.xpath('//div[@id="global_site"]//div[@class="in back_primary shadow_box"]/p//text()').extract()  
        if (len(game_description) > 0): 
            game_description = list(map(str.strip, game_description))
            if '...Read More' in game_description:
                game_description.remove('...Read More')
            game_description = ' '.join(game_description)

        game_name_alias = None
        systems_available = None
        game_genres = None
        north_america_release_date = None

        game_details = response.xpath('//div[@id="global_site"]//div[@class="in back_primary shadow_box"]/div/div') 

        for game_detail in game_details:
            game_detail_fields = game_detail.xpath('.//text()').extract()
            game_detail_fields = list(map(str.strip, game_detail_fields))
            while '' in game_detail_fields:
                game_detail_fields.remove('') 

            if (game_detail_fields[0] == 'Alias:'):
                game_name_alias = game_detail_fields[1]
            elif (game_detail_fields[0] == 'Playable On:'):
                systems_available = game_detail_fields[1]
            elif ((game_detail_fields[0] == 'Genres:') | (game_detail_fields[0] == 'Genre:')):
                game_genres = game_detail_fields[1]
            elif (game_detail_fields[0] == 'NA:'):
                north_america_release_date = game_detail_fields[1]

        item = HowlongtobeatItem()
        item['game_name'] = game_name
        item['game_id'] = response.meta['game_id']
        item['average_rating'] = average_rating
        item['rating_count'] = rating_count

        item['time_to_beat_main_story'] = time_to_beat_main_story
        item['time_to_beat_main_story_count'] = time_to_beat_main_story_count
        item['time_to_beat_main_story_rushed'] = time_to_beat_main_story_rushed
        item['time_to_beat_main_story_leisure'] = time_to_beat_main_story_leisure

        if (time_to_beat_main_extras):
            item['time_to_beat_main_extras'] = time_to_beat_main_extras
            item['time_to_beat_main_extras_count'] = time_to_beat_main_extras_count
            item['time_to_beat_main_extras_rushed'] = time_to_beat_main_extras_rushed
            item['time_to_beat_main_extras_leisure'] = time_to_beat_main_extras_leisure

        if (time_to_beat_completionist):
            item['time_to_beat_completionist'] = time_to_beat_completionist
            item['time_to_beat_completionist_count'] = time_to_beat_completionist_count
            item['time_to_beat_completionist_rushed'] = time_to_beat_completionist_rushed
            item['time_to_beat_completionist_leisure'] = time_to_beat_completionist_leisure

        if (game_name_alias):
            item['game_name_alias'] = game_name_alias
        if (systems_available):
            item['systems_available'] = systems_available
        if (game_genres):
            item['game_genres'] = game_genres
        if (north_america_release_date):
            item['north_america_release_date'] = north_america_release_date
        if (game_description):
            item['game_description'] = game_description

        yield item

    # Some counts stored as string, e.g. "1.7k"
    def convert_user_count_to_float(self, user_count_to_convert):
        user_count_to_convert = user_count_to_convert.strip()
        if (user_count_to_convert[-1] == 'K'):
            user_count_to_convert = float(user_count_to_convert[:-1]) * 1000
        else:
            user_count_to_convert = float(user_count_to_convert)

        return user_count_to_convert

    # Convert all playtimes from "27h 45m" to minutes in int for comparisons
    def convert_game_time_to_minutes(self, game_time_to_convert):
        game_time_to_convert = game_time_to_convert.strip()
        time_to_beat = re.findall('(\d+[hm]?) ?(\d*m?)', game_time_to_convert)
        time_in_minutes = 0
        for time in time_to_beat[0]:
            if(time == ''):
                continue
            elif (time[-1] == 'h'):
                time_in_minutes += int(time[:-1]) * 60
            else:
                time_in_minutes += int(time[:-1])

        return time_in_minutes

