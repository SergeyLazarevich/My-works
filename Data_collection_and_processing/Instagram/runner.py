from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Instagram import settings
from Instagram.spiders.instagram import InstagramSpider

if __name__ == '__main__':

    crawler_settings = Settings()  # создание класса для парсинга настроек
    crawler_settings.setmodule(settings)  # передача файла настроек

    process = CrawlerProcess(settings=crawler_settings)  # создание класса для парсинга сайта
    process.crawl(InstagramSpider)  # создание паука

    process.start()  # старт парсинга


