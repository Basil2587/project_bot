#  Telegram-боты

Что­бы создать бота, нам нужно дать ему название, адрес и получить токен — строку,
 которая будет однозначно идентифицировать нашего бота для серверов Telegram. 
 Зайдем в Telegram под своим аккаунтом и откроем «отца всех ботов», BotFather.

Жмем кноп­ку «Запустить» (или отправим /start), в ответ BotFather пришлет нам список доступных команд:

- /newbot — создать нового бота;
- /mybots — редактировать ваших ботов;
- /setname — сменить имя бота;
- /setdescription — изменить описание бота;
- /setabouttext — изменить информацию о боте;
- /setuserpic — изменить фото аватарки бота;
- /setcommands — изменить список команд бота;
- /deletebot — удалить бота.


# Инструкция 
1. Перейти в каталог с проектом и создать виртуальное окружение (`python3 -m venv venv`)
2. Запустить виртуальное окружение (`source venv/bin/activate`) на Mac/Linux или (`source venv/Scripts/activate`) на Windows
3. Установить все необходимые пакеты, указанные в файле requirements.txt (`pip install -r requirements.txt`)
4. В директории проекта создайте файл .env с токенами бота:
- TOKEN_ECHO_BOT=TOKEN
- TOKEN_FACTS_BOT=TOKEN
- TOKEN_GIRL_BOT=TOKEN


## Стек
 
Python 3, GIT

