import asyncio
from urllib.parse import urljoin

import aiohttp
import requests
from lxml import html


BASE_URI = 'https://www.countryflags.io/'


async def get_image(flag):
    async with aiohttp.ClientSession() as session:
        async with session.get(urljoin(BASE_URI, f'{flag}/flat/64.png')) as resp:
            with open(f'i_img/{flag}.png', 'wb') as f:
                print(f'Saving {flag}.png')
                f.write(await resp.read())


async def main(flags):
    await asyncio.gather(
        *[get_image(flag) for flag in flags]
    )

if __name__ == "__main__":
    flags = [
        x.xpath("./p[contains(@class, 'bold')]/text()")[0]
        for x in html.fromstring(requests.get(
            BASE_URI, 
            headers={'User-Agent': 'Mozzila/11.0'}
        ).text).xpath('//*[@id="countries"]/div/div/div')
    ]

    asyncio.run(main(flags))
