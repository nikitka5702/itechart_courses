# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_temperature(value):
    val, = value
    return val.replace('−', '-')


class YandexWeatherItem(scrapy.Item):
    city = scrapy.Field()
    temperature = scrapy.Field(serializer=serialize_temperature)
