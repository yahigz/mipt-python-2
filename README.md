# Останин Андрей Б05-325
# Телеграм-бот RuEGEBot

## Цель: 
### Создать телеграм-бота с тестовыми упражнениями из ЕГЭ по русскому языку.

## Функционал:
#### Есть несколько упражнений: ударения, пре/при, орфограммы в суффиксах, орфограммы на стыках приставки и корня. При этом у каждого пользователя есть свой счет. Его можно сбросить. Также можно узнать топ-10 пользователей с наибольшим счетом.

## Архитектура:
    - Используются библиотеки telebot, random, aiogram.types

    - Файл data.py содержит код для поддержания работы с данными пользователей

        - int CORRECT_ANSWER_INCREMENT, int INCORRECT_ANSWER_DECREMENT - как изменяется счет при правильном ответе

        - В файле users.txt хранится информация о пользователях - их id, имя и счёт.

        - Класс User: - пользователь
            - int id - id пользователя
            - str name - имя пользователя
            - int score - счет пользователя

            - __init__() - создать пользователя. По умолчанию имя каждого пользователя - "Abobus#____", где вместо ____ выбирается  случайное четырехзначное число
            - def correct_answer() - увеличить счет пользователя на CORRECT_ANSWER_INCREMENT
            - def incorrect_answer() - уменьшить счет пользователя на INCORRECT_ANSWER_DECREMENT

        - Класс UserDatabase: - здесь хранится информация о пользователях 
            - dict users - по id пользователя можно получить информацию о нём
            - list top_users

            - __init__() - загружаются данные из users.txt
            - def sync_file() - синхронизировать users.txt с текущей информацией о пользователях
            - def update_top() - обновить топ
            - def add_user(User) - добавить пользователя в базу
        
    - Файл app.py содержит код для поддержания логики работы бота

        - UserDatabase users

        - В файле emphasis.txt хранятся упражнения для ударений в формате абоба Абоба абОба абобА, где Абоба - правильный вариант ответа
        - В файле prepri.txt хранятся упражнения для пре/при в формате пр_абоба Е, преабоба - правильный вариант ответа
        - В файле suffix.txt хранятся упражнения для суффиксов в формате абоб_к И, абобик - правильный вариант ответа
        - В файле prefix.txt хранятся упражнения для приставок в формате д_абоба О, доабоба - правильный вариант ответа

        class Exercise:
            - str question - вопрос, который выведется 
            - str answer - ожидаемый ответ
            - list variants - варианты ответа 

            - __init__(int type) - type - тип упражнения - type = 0 - ударения, type = 1 - пре/при, type = 2 - остальное. type определяет, что будет в variants

        - def extract_exercises(str path) - выгружает содержимое файла в список упражнений
        - def extract_exercises_emphasis(str path) - выгружает содержимое файла в список упражнений для ударений

        - list EmphasisExercises
        - list PrePriExercises
        - list SuffixExercises
        - list PrefixExercises

        - list wait_list - список пользователей с необработанными запросами
        - dict type - какой статус у пользователя. 0 - ударение, 1 - пре/при, 3 - смена имени, 2 - остальное

        - @bot.message_handler(commands=["score"])
        def score(user) - выводит текущий счет пользователя

        - @bot.message_handler(commands=["emphasis"])
        def emphasis(user) - запускает упражнения на ударения

        - @bot.message_handler(commands=["prepri"])
        def prepri(user) - запускает упражнения на пре/при

        - @bot.message_handler(commands=["suffix"])
        def suffix(user) - запускает упражнения на суффиксы

        - @bot.message_handler(commands=["prefix"])
        def prefix(user) - запускает упражнения на приставки

        - @bot.message_handler(commands = ["rating"])
        def rating(user) - выводит топ10

        - @bot.message_handler(commands = ["rename"])
        def rename(user) - переименовывает пользователя

        - @bot.message_handler(commands = ["reset"])
        def reset(user) - сбрасывает счет пользователя

        - @bot.message_handler(commands = ["sync_file_z9bmiMjuK9wFyEXOCBFMzVwqBAAlDdt8"])
        def sync() - вызывает sync_file() для базы упражнений. команда только для админа

        - @bot.message_handler(content_types = ["text"])
        def check(message) - обрабатывает ответ на упражнение/ренейм

        - @bot.message_handler(commands = ["start"])
        def start(user) - выводит меню
