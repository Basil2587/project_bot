import asyncio
import os
import platform
import re
import telebot
import wikipedia
from dotenv import load_dotenv

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TOKEN_ECHO_BOT'))
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")


# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def get_wiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wiki_text = ny.content[:1000]
        # Разделяем по точкам
        wiki_mas = wiki_text.split('.')
        # Отбрасываем всё после последней точки
        wiki_mas = wiki_mas[:-1]
        # Создаем пустую переменную для текста
        wiki_text2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wiki_mas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные
                # при разделении строк точки на место
                if len((x.strip())) > 3:
                    wiki_text2 = wiki_text2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wiki_text2 = re.sub('/([^()]*/)', '', wiki_text2)
        wiki_text2 = re.sub('/([^()]*/)', '', wiki_text2)
        wiki_text2 = re.sub('/{[^/{/}]*/}', '', wiki_text2)
        # Возвращаем текстовую строку
        return wiki_text2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, get_wiki(message.text))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
