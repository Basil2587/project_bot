import asyncio
import platform

import requests

import telebot
import os
import time
from multiprocessing.context import Process
import schedule
from bs4 import BeautifulSoup
from pathlib import Path
from random import choice
from glob import glob
from requests import get
from telebot import types
from fuzzywuzzy import fuzz
from dotenv import load_dotenv


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

# Парсим сайт и вытаскиваем картинки
site = 'https://yandex.ru/images/search?from=tabbar&text=%D1%81%D0%B8%D1%81%D1%8C%D0%BA%D0%B8'
response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]
urls = list(filter(None, urls))

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TOKEN_GIRL_BOT'))

# Загружаем список фраз и ответов в массив
list_phrases = []
if os.path.exists('data/b2.txt'):
    file_path = open('data/b2.txt', 'r', encoding='UTF-8')
    for x in file_path:
        if len(x.strip()) > 2:
            list_phrases.append(x.strip().lower())
    file_path.close()


# С помощью fuzzywuzzy вычисляем наиболее похожую фразу и выдаем в качестве ответа следующий элемент списка
def answer_question(text):
    try:
        text = text.lower().strip()
        if os.path.exists('data/b2.txt'):
            a = 0
            n = 0
            nn = 0
            for q in list_phrases:
                if 'u: ' in q:
                    # С помощью fuzzywuzzy получаем, насколько похожи две строки
                    string_comparison = (fuzz.token_sort_ratio(q.replace('u: ', ''), text))
                    if string_comparison > a and string_comparison != a:
                        a = string_comparison
                        nn = n
                n = n + 1
            similar_phrase = list_phrases[nn + 1]
            return similar_phrase
        else:
            return 'Ошибка'
    except:
        return 'Ошибка'


# Команда start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Сиськи", "Показать фото с сервера"]
    markup.add(*buttons)
    # bot.send_message(m.chat.id, 'Я на связи. Напиши мне Привет )')
    bot.send_message(message.chat.id, '\nЯ на связи. Напиши мне Привет или\n'
                                      'Нажмите: \nНа кнопку', reply_markup=markup)


@bot.message_handler(commands=["game"])
def spn_game(message):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton("Камень", callback_data="камень"),
               types.InlineKeyboardButton("Бумага", callback_data="бумага"),
               types.InlineKeyboardButton("Ножницы", callback_data="ножницы")]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, "Выберите 'камень', 'бумага', 'ножницы' ", reply_markup=keyboard)


# Получение сообщений от юзера
@bot.message_handler(content_types=["photo"])
def handle_image(message):
    size_folder = sum([f.stat().st_size for f in Path("image", "photos").glob("**/*")])
    mb = size_folder / 1000000
    try:
        if mb < 30:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = str(Path('image')) + '/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Фото получил, обрабатываю...")
        else:
            bot.reply_to(message, "Много фоток...")
        if mb > 30:
            path = 'image/photos/'
            sorted_file = sorted(((os.path.getctime(name), name) for name in os.listdir() if os.path.isfile(name)))
            early_file = sorted_file[0][1]
            os.remove(path + early_file)

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Запись логов
    new_file_path = open('data/' + str(message.chat.id)
                         + '_' + str(message.chat.username) + '_log.txt', 'a', encoding='UTF-8')
    if message.text.lower() == 'сиськи':
        picture_site = choice(urls)
        get_img = get('https:' + picture_site).content
        bot.send_photo(message.chat.id, get_img)
    elif message.text.lower() == 'показать фото с сервера':
        lists = glob('image/photos/*')  # создаем список из названий картинок
        picture = choice(lists)
        bot.send_photo(message.chat.id, photo=open(picture, 'rb'))

    else:
        text_answer = answer_question(message.text)
        new_file_path.write('u: ' + message.text + '\n' + text_answer + '\n')
        new_file_path.close()
        # Отправка ответа
        bot.send_message(message.chat.id, text_answer)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    game_dict = {"камень": '🪨', "бумага": '📃', "ножницы": '✂'}
    word_list = [i for i in game_dict.keys()]
    computer_action = choice(word_list)
    if call.data == computer_action:
        bot.answer_callback_query(
            call.id, text=f"Я выбрала {computer_action} {game_dict[computer_action]}.\n Ничья!!", show_alert=True)
    elif call.data == "камень":
        if computer_action == "ножницы":
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action}{game_dict[computer_action]}.\n Камень бьет ножницы! Вы победили!",
                show_alert=True)
        else:
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action}{game_dict[computer_action]}.\n"
                     f" Бумага оборачивает камень! Вы проиграли.", show_alert=True)
    elif call.data == "бумага":
        if computer_action == "камень":
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action}{game_dict[computer_action]}.\n"
                     f" Бумага оборачивает камень! Вы победили.", show_alert=True)
        else:
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action} {game_dict[computer_action]}.\n"
                     f" Ножницы режут бумагу! Вы проиграли.", show_alert=True)
    elif call.data == "ножницы":
        if computer_action == "бумага":
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action} {game_dict[computer_action]}.\n"
                     f"Ножницы режут бумагу! Вы победили!", show_alert=True)
        else:
            bot.answer_callback_query(
                call.id,
                text=f"Я выбрала {computer_action} {game_dict[computer_action]}.\n"
                     f"Камень бьет ножницы! Вы проиграли.", show_alert=True)


# Отправка фото, сообщение по времени
def send_message1():
    picture = choice(urls)
    site_img = get('https:' + picture).content
    bot.send_photo(485409413, site_img)
    # bot.send_message(1286749978, 'TEXT')


def send_message2():
    bot.send_message(485409413, 'Доброе утро!')


def send_message3():
    bot.send_message(485409413, 'Ты красавчик!!!')


schedule.every(60).minutes.do(send_message1)
schedule.every().day.at("09:00").do(send_message2)
schedule.every().day.at("17:00").do(send_message3)


class ScheduleMessage():
    def send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process():
        p1 = Process(target=ScheduleMessage.send_schedule, args=())
        p1.start()


# Запускаем бота
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
