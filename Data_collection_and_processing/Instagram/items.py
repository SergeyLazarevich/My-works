# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import TakeFirst
import scrapy


class InstagramItem(scrapy.Item):
    """
        Класс предобработки данных
    """
    _id = scrapy.Field(output_processor=TakeFirst())
    follow_list = scrapy.Field(output_processor=TakeFirst())
    fol_username = scrapy.Field(output_processor=TakeFirst())
    fol_user_id = scrapy.Field(output_processor=TakeFirst())
    pic_url = scrapy.Field(output_processor=TakeFirst())
    j_body = scrapy.Field(output_processor=TakeFirst())
    username = scrapy.Field(output_processor=TakeFirst())
    user_id = scrapy.Field(output_processor=TakeFirst())
