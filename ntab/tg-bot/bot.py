import asyncio
import datetime
import logging
import pathlib
from typing import List, Union
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_media_group import media_group_handler
from database import UserDB
from config import telegram_channels, web_sources, sender
from neuronet.FinalProject.news_handler import NewsHandler
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated

news = []
db = UserDB()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6719902391:AAFq9Bx40bUYUagH0R7-plCfxcmNNH90XaU")
# Диспетчер
dp = Dispatcher()
# Проверятель новостей
newshandler = NewsHandler()


#для ключевой метрики (пользователь заблокировал бота)
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    print(event.from_user.id, datetime.datetime.now())


async def send_text(message: types.Message):
    has_text = newshandler.return_result(message.text)
    if has_text:
        return

    for user in db.get_users_id():
        for i in range(0, len(message.text), 1000):
            await bot.send_message(user[0], message.text[i:i + 1000], entities=message.entities)


async def send_media(message: types.Message, group_builder: MediaGroupBuilder):
    has_caption = newshandler.return_result(group_builder.caption)
    if has_caption:
        return

    message_build = group_builder.build()
    for user in db.get_users_id():
        await bot.send_media_group(user[0], media=message_build)
        if message.caption == None:
            continue

        for i in range(1000, len(message.caption), 1000):
            await bot.send_message(user[0], message.caption[i:i + 1000], entities= message.caption_entities)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    #для ключевой метрики (время подключения)
    start = datetime.datetime.now()
    print(message.from_user.id)
    # здесь встроить БД
    media_group = MediaGroupBuilder(caption='!elloH')
    text_file = types.FSInputFile(pathlib.Path(__file__).parent.joinpath('ecxo9agd.png'))
    media_group.add_photo(text_file)
    db.add_user(message.from_user.id, [""], [""])
    await bot.send_media_group(message.from_user.id, media=media_group.build())


@dp.message(Command("base_sources"))
async def cmd_print_base_sources(message: types.Message):
    channels_links = 'Телеграмм-источники:\n' + '\n'.join([f"{link}" for link in telegram_channels.values()])
    web_links = '\nИнтернет-ресурсы:\n' + '\n'.join([f"{source}" for source in web_sources])
    sources = channels_links + web_links
    await bot.send_message(message.from_user.id, sources)


async def add_in_builder(message: types.Message, group_builder: MediaGroupBuilder):
    if message.caption:
        group_builder.caption = message.caption[:1000]
        if message.caption_entities:
            group_builder.caption_entities = [ent for ent in message.caption_entities if
                                              (ent.offset + ent.length) < 1000]

    if message.audio:
        group_builder.add_audio(message.audio.file_id)

    if message.document:
        group_builder.add_document(message.document.file_id)

    if message.photo:
        group_builder.add_photo(message.photo[-1].file_id)

    if message.video:
        group_builder.add_video(message.video.file_id)


@dp.message(F.media_group_id == None)
async def simple_message(message: types.Message):
    if message.from_user.id not in [sender, 1836363817]:
        print('Такой функциональности у меня нет')
        return

    if message.text:
        await send_text(message)
        return

    group_builder = MediaGroupBuilder()
    await add_in_builder(message, group_builder)
    await send_media(message, group_builder)


@dp.message(F.media_group_id)
@media_group_handler
async def media_group_message(messages: list[types.Message]):
    if messages[0].from_user.id not in [sender, 1836363817]:
        print('Такой функциональности у меня нет')
        return

    group_builder = MediaGroupBuilder()
    for message in messages:
        await add_in_builder(message, group_builder)
    await send_media(message, group_builder)


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())