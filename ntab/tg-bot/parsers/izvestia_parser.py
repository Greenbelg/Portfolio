import aiohttp
from bs4 import BeautifulSoup
from collections import deque


class RGParser:
    def __init__(self):
        self._url_main_page = "https://rg.ru/region/urfo/sverdlovskobl/ekaterinburg/"
        self._queue = deque(maxlen=10)

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url_main_page) as response:
                main_page = await response.text()
                soup = BeautifulSoup(main_page, "lxml")
                links = soup.find_all("div", {"class": "ItemOfListStandard_wrapper__bO1Hw"})
                for link in links:
                    msg = link.text
                    try:
                        contents = link.contents[-1]
                        link_for_news = contents.get('href')
                    except AttributeError:
                        continue
                    if link_for_news is not None and not link_for_news.startswith(self._url_main_page):
                        link_for_news = self._url_main_page + link_for_news
                    if link_for_news in self._queue:
                        continue
                    self._queue.appendleft(link_for_news)
                    yield msg, link_for_news
