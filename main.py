import logging
import asyncio
from datetime import datetime
import re
import sqlite3

from aiogram import Bot, Dispatcher, executor, types

from config import token, chat_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)


async def check_reminder():
    while True:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM reminders")
        users_ids = [i[0] for i in cursor.fetchall()]

        for current_id in users_ids:
            cursor.execute(f"SELECT reminder_time FROM reminders WHERE user_id = '{current_id}'")
            reminders = cursor.fetchall()
            for reminder_time in reminders:
                if datetime.now().strftime("%H:%M") == reminder_time:
                    await bot.send_message(current_id, "Reminder")
                    await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)


@dp.message_handler(commands=['start', 'register'])
async def send_welcome(message: types.Message):
    asyncio.create_task(check_reminder())
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(user_id, username) VALUES(?,?)', (message.chat.id, message.from_user.username))
    connection.commit()
    await message.reply("whatever")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я когда-нибудь тебе расскажу, что я могу, но не сейчас")


@dp.message_handler(commands=['set'])
async def set_reminder(message: types.Message):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    text = message.get_args()
    if re.fullmatch(r'\d\d:\d\d', text):
        cursor.execute(f"SELECT * FROM reminders WHERE user_id = '{message.chat.id}'")
        user_reminders = [i[1] for i in cursor.fetchall()]
        if text in user_reminders:
            await message.answer("Такое время уже есть")
        else:
            cursor.execute(f'INSERT INTO reminders VALUES(?, ?)', (message.chat.id, text))
            connection.commit()
            await message.answer("Успешно задано")
    else:
        await message.answer("Ведите время напоминания")


@dp.message_handler(commands=['delete'])
async def delete_reminder(message: types.Message):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    text = message.get_args()
    if re.fullmatch(r'\d\d:\d\d', text):
        cursor.execute(f"SELECT * FROM reminders WHERE user_id = '{message.chat.id}'")
        user_reminders = [i[1] for i in cursor.fetchall()]
        if text not in user_reminders:
            await message.answer("Такого времени нет")
        else:
            cursor.execute(f"DELETE FROM reminders WHERE user_id =  '{message.chat.id}' and reminder_time = '{text}'")
            connection.commit()
            await message.answer("Успешно удалено")
    else:
        await message.answer("Ведите время напоминания")


@dp.message_handler(commands=['get_all'])
async def send_reminders(message: types.Message):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM reminders WHERE user_id = '{message.chat.id}'")
    user_reminders = [i[1] for i in cursor.fetchall()]
    if len(user_reminders) == 0:
        await message.answer("Не задано ни одного напоминания")
    else:
        ans = ""
        for i in range(len(user_reminders)):
            ans = str(i) + " " + user_reminders[i] + "\n"
        await message.answer(ans)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    await message.answer("Я такое не ем")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
