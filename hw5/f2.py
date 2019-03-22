from urllib.request import urlopen

from lxml.html import parse


page = parse(urlopen('https://yandex.by/pogoda/region/149'))

data = {}

for column in page.xpath('//div[contains(@class, "grid__row")]/div'):
    data.update({item.xpath('./a/text()')[0]: int(item.xpath('./span/text()')[0].replace('−', '-')) for items in column.xpath('./div') for item in items.xpath('./ul/li')})


print(data)
