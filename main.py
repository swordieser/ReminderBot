import logging
import asyncio
from datetime import datetime
import re

from aiogram import Bot, Dispatcher, executor, types

from config import token, chat_id

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

reminders = []


async def check_reminder():
    while True:
        for reminder_time in reminders:
            if datetime.now().strftime("%H:%M") == reminder_time:
                await bot.send_message(chat_id, "Reminder")
        await asyncio.sleep(60)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    asyncio.create_task(check_reminder())
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Я когда-нибудь тебе расскажу, что я могу, но не сейчас")


@dp.message_handler(commands=['set'])
async def set_reminder(message: types.Message):
    text = message.get_args()
    if re.fullmatch(r'\d\d:\d\d', text):
        if text in reminders:
            await message.answer("Такое время уже есть")
        else:
            reminders.append(text)
            await message.answer("Успешно задано")
    else:
        await message.answer("Ведите время напоминания")


@dp.message_handler(commands=['delete'])
async def delete_reminder(message: types.Message):
    text = message.get_args()
    if re.fullmatch(r'\d\d:\d\d', text):
        if text not in reminders:
            await message.answer("Такого времени нет")
        else:
            reminders.remove(text)
            await message.answer("Успешно удалено")
    else:
        await message.answer("Ведите время напоминания")


@dp.message_handler(commands=['get_all'])
async def send_reminders(message: types.Message):
    if len(reminders) == 0:
        await message.answer("Не задано ни одного напоминания")
    else:
        ans = ""
        for i in range(len(reminders)):
            ans = str(i) + " " + reminders[i] + "\n"
        await message.answer(ans)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    await message.answer("Я такое не ем")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
