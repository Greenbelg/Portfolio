import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import deque


class AIFParser:
    def __init__(self):
        self._url_main_page = "https://ural.aif.ru"
        self._queue = deque(maxlen=10)
        self._classes_news = {"top_box", "bottom_item", "item_text"}

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url_main_page) as response:
                main_page = await response.text()

                soup = BeautifulSoup(main_page, "lxml")
                links = soup.find_all("ul", {"class": "list_js"})
                for link in links:
                    try:
                        contents0 = link.contents
                    except AttributeError:
                        continue
                    for content0 in contents0:
                        if content0 != '\n':
                            try:
                                contents1 = content0.contents
                            except AttributeError:
                                continue
                            for content1 in contents1:
                                if content1 != '\n':
                                    link_for_news = content1.get("href")
                                    if link_for_news is None:
                                        continue
                                    if not link_for_news.startswith(self._url_main_page):
                                        link_for_news = self._url_main_page + link_for_news
                                    msg = content1.text

                                    if link_for_news in self._queue:
                                        continue
                                    self._queue.appendleft(link_for_news)
                                    yield msg, link_for_news


                for class_news in self._classes_news:
                    links = soup.find_all("div", {"class": f"{class_news}"})
                    for link in links:
                        msg = link.text
                        href_tag = link.contents[1]
                        link_for_news = href_tag.get("href")
                        if not link_for_news.startswith(self._url_main_page):
                            link_for_news = self._url_main_page + link_for_news
                        if link_for_news in self._queue:
                            continue
                        self._queue.appendleft(link_for_news)
                        yield msg, link_for_news


async def main():
    kp = AIFParser()
    i = 1
    async for data in kp.get_news():
        print(i, data)
        i += 1

if __name__ == "__main__":
    asyncio.run(main())