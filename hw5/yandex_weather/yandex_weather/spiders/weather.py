# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from yandex_weather.items import YandexWeatherItem


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['yandex.by']
    start_urls = ['https://yandex.by/pogoda/region/149']

    def parse(self, response):
        for column in response.xpath('//div[contains(@class, "grid__row")]/div'):
            for cities in column.xpath('./div'):
                for city in cities.xpath('./ul/li'):
                    yield response.follow(city.xpath('./a/@href').get(), callback=self.parse_city)

    def parse_city(self, response):
        item = ItemLoader(item=YandexWeatherItem(), response=response)
        item.add_xpath('city', '//ol[@class="breadcrumbs"]/li[3]/span[@class="breadcrumbs__title"]/text()')
        item.add_xpath('temperature', '//div[contains(@class, "temp fact__temp")]/span[@class="temp__value"]/text()')
        yield item.load_item()
