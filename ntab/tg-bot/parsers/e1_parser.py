import aiohttp
from bs4 import BeautifulSoup
from collections import deque


class E1Parser:
    def __init__(self):
        self._url_main_page = "https://www.e1.ru"
        self._queue = deque(maxlen=10)
        self._classes_news = {"Jstj9", "FYpgD moeZF", "-wwmz MM+zX"}

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url_main_page) as response:
                main_page = await response.text()

                soup = BeautifulSoup(main_page, "lxml")
                for class_news in self._classes_news:
                    links = soup.find_all("a", {"class": f"{class_news}"})
                    for link in links:
                        msg = link.text
                        link_for_news = link.get("href")
                        if not link_for_news.startswith(self._url_main_page):
                            link_for_news = self._url_main_page + link_for_news
                        if link_for_news in self._queue:
                            continue
                        self._queue.appendleft(link_for_news)
                        yield msg, link_for_news
