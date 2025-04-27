import asyncio
import logging
import sys
from os import getenv
from db import DBConnection

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import (
    CommandStart,
    Command,
    CommandObject,
)
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

db = DBConnection()

def add_user_to_db(user=None, group_id=None, message=None) -> None:
    if message is not None:
        group_id = message.chat.id
        user = message.from_user
    
    tag_name = user.username or (
        user.first_name + (f" {user.last_name}" if user.last_name else "")
    )
    
    try:
        db.add_user(user.id, group_id, tag_name)
    except:
        pass

# /start
@dp.message(CommandStart())
async def group_start_handler(message: Message) -> None:
    add_user_to_db(message=message)

    if message.chat.type in ["group", "supergroup"]:
        await message.answer("Привіт усім! Я прийомниш")
        chat_id = message.chat.id

        db.add_group(chat_id)
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("top"))
async def top_handler(message: Message) -> None:
    add_user_to_db(message=message)

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
    add_user_to_db(message=message)

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
    add_user_to_db(message=message)

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
    add_user_to_db(message=message)

    param = int(command.args)
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        db.set_time(chat_id, param)
        await message.answer("Таймер встановлено")
    else:
        # Якщо /start у приваті
        await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!")

@dp.callback_query(lambda c: c.data.startswith("quiz_answer"))
async def quiz_answer_handler(callback: CallbackQuery) -> None:
    user = callback.from_user
    user_id = user.id
    group_id = callback.message.chat.id

    add_user_to_db(user=user, group_id=group_id)

    splited_data = callback.data.split("_")

    if db.has_user_answered_question(user_id, group_id, int(splited_data[3])):
        await callback.answer("Ви вже відповіли на це питання!")
    else:
        db.add_user_answered_question(user_id, group_id, int(splited_data[3]))

        is_correct = int(splited_data[2])

        if is_correct:
            db.add_points(user_id, group_id, 1)
            await callback.answer("Правильна відповідь!")
        else:
            db.add_points(user_id, group_id, -1)
            await callback.answer("Неправильна відповідь!")


async def scheduler(bot) -> None:
    while True:  
        group_ids = db.get_groups_with_ended_period()

        for group_id in group_ids:
            question_data = db.get_question()
            question_id = question_data["question_id"]

            keyboard_answers = [[InlineKeyboardButton(text=answer, callback_data=f"quiz_answer_{'1' if question_data['correct_answer'] == answer else '0'}_{question_id}")] for answer in question_data["answers"]]
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_answers)

            await bot.send_message(group_id, question_data["question"], reply_markup=keyboard)

            db.set_last_message(group_id)

        group_ids = db.get_groups_with_ended_time()

        for group_id in group_ids:
            question_data = db.get_question()
            question_id = question_data["question_id"]

            keyboard_answers = [[InlineKeyboardButton(text=answer, callback_data=f"quiz_answer_{'1' if question_data['correct_answer'] == answer else '0'}_{question_id}")] for answer in question_data["answers"]]
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_answers)

            await bot.send_message(group_id, question_data["question"], reply_markup=keyboard)

            db.set_time(group_id, 0)

        await asyncio.sleep(5)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    asyncio.create_task(scheduler(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
