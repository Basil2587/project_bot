import asyncio
import os
import platform
import telebot
import random
from telebot import types

from dotenv import load_dotenv

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

# Загружаем список интересных фактов
f = open('data/facts.txt', 'r', encoding='UTF-8')
facts = f.read().split('\n')
f.close()
# Загружаем список поговорок
f = open('data/thinks.txt', 'r', encoding='UTF-8')
thinks = f.read().split('\n')
f.close()
# Создаем бота
bot = telebot.TeleBot(os.getenv('TOKEN_FACTS_BOT'))


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Факт")
    item2 = types.KeyboardButton("Поговорка")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,
                     'Нажмите: \nФакт для получения интересного факта\nПоговорка — для получения мудрой цитаты ',
                     reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1, выдаем ему случайный факт
    if message.text.strip() == 'Факт':
        answer = random.choice(facts)
        bot.send_message(message.chat.id, answer)
    # Если юзер прислал 2, выдаем умную мысль
    elif message.text.strip() == 'Поговорка':
        answer = random.choice(thinks)
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Вы написали: ' + message.text +
                         '\n Бот принимает только командные слова как "Факт" или "Поговорка"')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
