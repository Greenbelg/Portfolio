from collections import deque
from telethon import TelegramClient, events
import asyncio
import random
from parsers.kp_parser import KPParser
from parsers.e1_parser import E1Parser
from parsers.aif_parser import AIFParser
from parsers.sixsix_parser import S66Parser
from parsers.izvestia_parser import RGParser
from parsers.rambler_parser import RamblerParser
from parsers.uralweb_parser import UralwebParser
from parsers.vesti_ural_parser import VestyUralParser

from config import api_id, api_hash, telegram_channels

posted_news = deque()
telegram_channels_links = list(telegram_channels.values())


async def store_news(parser):
    await prepare_parsers(parser)
    while True:
        news = parser.get_news()
        async for new in news:
            text = new[0] + '\n\r\n\r' + f'Источник: {new[1]}'
            if is_repeating_news(text):
                continue
            print(text)
            await news_queue.put(text)
        
        await asyncio.sleep(random.uniform(4, 8))


async def send_news():
    while True:
        news_item = await news_queue.get()
        await client.send_message(entity='@NewsTransportAccidentsBot', message=news_item)
        news_queue.task_done()


def is_repeating_news(new):
    head = new[:50].strip()
    if head in posted_news:
        return True
    
    if len(posted_news) > 50000:
        posted_news.clear()
    
    posted_news.appendleft(head)
    return False


async def prepare_parsers(parser):
    news = parser.get_news()
    async for new in news:
        text = new[0] + '\n\r\n\r' + f'Источник: {new[1]}'
        if is_repeating_news(text):
            continue
        print(text)
        posted_news.appendleft(text)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    news_queue = asyncio.Queue(maxsize=100)
    client = TelegramClient('Somestring', api_id, api_hash, loop=loop)
    client.start()

    kpparser = KPParser()
    e1parser = E1Parser()
    aifparser = AIFParser()
    s66parser = S66Parser()
    izvestia_parser = RGParser()
    rambler_parser = RamblerParser()
    uralweb_parser = UralwebParser()
    vestyural_parser = VestyUralParser()

    loop.create_task(store_news(kpparser))
    loop.create_task(store_news(e1parser))
    loop.create_task(store_news(aifparser))
    loop.create_task(store_news(s66parser))
    loop.create_task(store_news(izvestia_parser))
    loop.create_task(store_news(rambler_parser))
    loop.create_task(store_news(uralweb_parser))
    loop.create_task(store_news(vestyural_parser))
    loop.create_task(send_news())


    @client.on(events.NewMessage(chats=telegram_channels_links))
    async def handler(event):
        if event.raw_text == '':
            return

        news_text = ' '.join(event.raw_text.split('\n')[:2])
        if is_repeating_news(news_text):
            return

        await client.send_message(entity='@NewsTransportAccidentsBot', message=event.message)


    client.run_until_disconnected()