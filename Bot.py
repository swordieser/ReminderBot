import telebot
from telebot import types
from datetime import datetime
import re
from threading import Thread
import time

f = open("bot_token.txt")
token = f.readline()
f.close()

bot = telebot.TeleBot(token)

times = ["9:00", "15:00", "15:30", "21:00", "21:30"]

chat_id = 401765772


def remind():
    while True:
        for reminder_time in times:
            if datetime.now().time().strftime("%H:%M") == reminder_time:
                bot.send_message(chat_id, "Напоминание")
        time.sleep(60)


@bot.message_handler(commands=["start"])
def start(message, res=False):
    if message.chat.id == chat_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Задать время напоминания")
        item2 = types.KeyboardButton("Посмотреть времена напоминания")
        item3 = types.KeyboardButton("Удалить времена напоминания")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(chat_id, "Выберите опцию", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.id == chat_id:
        if message.text.strip() == "Задать время напоминания":
            bot.send_message(chat_id, "Введите время")

        elif message.text.strip() == "Посмотреть времена напоминания":
            ans = ""
            for index, reminder_time in enumerate(times):
                ans += "Напоминание номер: " + str(index) + ", время напоминания: " + reminder_time + "\n"

            bot.send_message(chat_id, ans)

        elif message.text.strip() == "Удалить времена напоминания":
            bot.send_message(chat_id, "Введите номер")

        elif re.match(r"\d\d:\d\d", message.text.strip()) is not None and \
                message.text.strip() == re.match(r"\d\d:\d\d", message.text.strip()).group(0):

            times.append(message.text.strip())

            bot.send_message(chat_id, "Добавлено: " + message.text.strip())

        elif re.match(r"\d+", message.text.strip()) is not None and \
                message.text.strip() == re.match(r"\d+", message.text.strip()).group(0):

            del times[int(message.text.strip())]

            ans = "Оставшиеся времена:\n"
            for index, reminder_time in enumerate(times):
                ans += str(index) + " " + reminder_time + "\n"
            bot.send_message(chat_id, ans)


def start_bot():
    th = Thread(target=remind())
    th2 = Thread(target=bot.polling(none_stop=True, interval=0))
    th.start()
    th2.start()
