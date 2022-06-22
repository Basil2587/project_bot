import asyncio
import os
import platform

import telebot
from dotenv import load_dotenv


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()


# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TOKEN_ECHO_BOT'))
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
