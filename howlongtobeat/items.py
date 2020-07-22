# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HowlongtobeatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name = scrapy.Field()
    game_ID = scrapy.Field()

    time_to_beat_main_story = scrapy.Field()
    time_to_beat_main_story_count = scrapy.Field()
    time_to_beat_main_story_rushed = scrapy.Field()
    time_to_beat_main_story_leisure = scrapy.Field()

    time_to_beat_main_extras = scrapy.Field()
    time_to_beat_main_extras_count = scrapy.Field()
    time_to_beat_main_extras_rushed = scrapy.Field()
    time_to_beat_main_extras_leisure = scrapy.Field()

    time_to_beat_completionist = scrapy.Field()
    time_to_beat_completionist_count = scrapy.Field()
    time_to_beat_completionist_rushed = scrapy.Field()
    time_to_beat_completionist_leisure = scrapy.Field()

    average_rating = scrapy.Field()
    rating_count = scrapy.Field()

    game_genres = scrapy.Field()
    game_name_alias = scrapy.Field()
    game_description = scrapy.Field()
    systems_available = scrapy.Field()
    north_america_release_date = scrapy.Field()

