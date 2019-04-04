from multiprocessing import Pool
from urllib.parse import urljoin

import requests
from lxml import html


BASE_URI = 'https://www.countryflags.io/'

session = requests.Session()


def get_image(flag):
    response = session.get(urljoin(BASE_URI, f'{flag}/flat/64.png'))
    with open(f'i_img/{flag}.png', 'wb') as f:
        print(f'Saving {flag}.png')
        f.write(response.content)


if __name__ == '__main__':
    flags = [
        x.xpath("./p[contains(@class, 'bold')]/text()")[0]
        for x in html.fromstring(requests.get(
            BASE_URI, 
            headers={'User-Agent': 'Mozzila/11.0'}
        ).text).xpath('//*[@id="countries"]/div/div/div')
    ]

    with Pool(32) as p:
        p.map(get_image, flags)
