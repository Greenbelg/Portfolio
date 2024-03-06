import re
import aiohttp
from bs4 import BeautifulSoup
from collections import deque


class KPParser:
    def __init__(self):
        self._url_main_page = "https://www.ural.kp.ru"
        self._queue = deque(maxlen=10)

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url_main_page) as response:
                main_page = await response.text()

                soup = BeautifulSoup(main_page, "lxml")
                links = soup.find_all("a", {"class": re.compile("sc-1tputnk-2.*")})
                links_for_photo_news = soup.find_all("div", {"class": re.compile("sc-10r6yic-2.*")})

                tasks = []
                for link, link_for_photo_news in zip(links, links_for_photo_news):
                    msg = link.text
                    link_for_news = link.get("href")
                    if not link_for_news.startswith(self._url_main_page):
                        link_for_news = self._url_main_page + link_for_news
                    if link_for_news in self._queue:
                        continue
                    self._queue.appendleft(link_for_news)
                    # task = asyncio.ensure_future(self._get_photo(session, link_for_photo_news.contents))
                    tasks.append((msg, link_for_news)) # task))

                # results = await asyncio.gather(*[task[2] for task in tasks])
                for i, (msg, link, _) in enumerate(tasks):
                    yield msg, link # , results[i]

    async def _get_photo(self, session, contents, depth=4):
        if depth == 0:
            for content in contents:
                url = content.get("src")
                if url is not None:
                    if not url.startswith("https"):
                        url = "https:" + url
                    async with session.get(url) as response:
                        photo = await response.read()
                        return photo
            return

        for content in contents:
            try:
                photo = await self._get_photo(session, content.contents, depth - 1)
                return photo
            except AttributeError:
                continue
