import asyncio
import logging
import sys
from os import getenv
from db import DBConnection

import psycopg2
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import (
    CommandStart,
    Command,
    ChatMemberUpdatedFilter,
    CommandObject,
)
from aiogram.types import (
    Message,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

db = DBConnection()


def add_user_to_db(message):
    group_id = message.chat.id
    user = message.from_user
    tag_name = user.username or (
        user.first_name + (f" {user.last_name}" if user.last_name else "")
    )
    try:
        db.add_user(user.id, group_id, tag_name)
    except:
        pass


def add_group_to_db(group_id):
    db.add_group(group_id)


def join_button():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Приєднатися", callback_data="join_quiz")]
        ]
    )
    return keyboard


# /start
@dp.message(CommandStart())
async def group_start_handler(message: Message) -> None:
    if message.chat.type in ["group", "supergroup"]:
        await message.answer("Привіт усім! Я прийомниш")
        chat_id = message.chat.id

        print(chat_id)

        add_group_to_db(chat_id)
        await message.answer(
            "Хочеш взяти участь у вікторині? Натисни кнопку нижче",
            reply_markup=join_button(),
        )
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")


# def add_user_decorator(func):
#     def wrapper(message):
#         user = message.from_user
#         chat_id = message.chat.id
#         add_user_to_db(user, chat_id)
#         return func(message)

#     return wrapper


# /top
@dp.message(Command("top"))
async def top_handler(message: Message) -> None:
    add_user_to_db(message)
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        result = db.get_top(chat_id)
        await message.answer(
            "\n".join([f"{user['tag_name']}, {user['points']}" for user in result])
        )
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")


# /my_rating
@dp.message(Command("my_rating"))
async def top_handler(message: Message) -> None:
    add_user_to_db(message)
    if message.chat.type in ["group", "supergroup"]:
        user_id = message.from_user.id
        chat_id = message.chat.id
        result = db.get_my_rating(user_id, chat_id)
        await message.answer(f"{result}")
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")


# /set_period
@dp.message(Command("set_period"))
async def top_handler(message: Message, command: CommandObject) -> None:
    add_user_to_db(message)
    param = int(command.args)
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        db.set_period(chat_id, param)
        await message.answer("Період встановлено")
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")


# /set_time
@dp.message(Command("set_time"))
async def top_handler(message: Message, command: CommandObject) -> None:
    add_user_to_db(message)
    param = int(command.args)
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        db.set_time(chat_id, param)
        await message.answer("Таймер встановлено")
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")


# Обробка натискання на кнопку "Приєднатися"
@dp.callback_query(F.data == "join_quiz")
async def handle_join_quiz(callback: CallbackQuery, bot: Bot):
    user = callback.from_user
    chat_id = callback.message.chat.id

    add_user_to_db(user, chat_id)

    await bot.send_message(chat_id, f"{html.bold(user.full_name)} додано до вікторини!")

    await callback.answer("Ти приєднався!")


# Старт бота
async def scheduler() -> None:
    while True:  
        db.is_period()
        db.is_time()
        await asyncio.sleep(5)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
