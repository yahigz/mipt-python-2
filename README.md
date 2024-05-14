# Останин Андрей Б05-325
# Телеграм-бот RuEGEBot

## Цель: 
### Создать телеграм-бота с тестовыми упражнениями из ЕГЭ по русскому языку.

## Функционал:
#### Есть несколько упражнений: ударения, пре/при, орфограммы в суффиксах, орфограммы на стыках приставки и корня. При этом у каждого пользователя есть свой счет. Его можно сбросить. Также можно узнать топ-10 пользователей с наибольшим счетом.

## Архитектура:
    - Используются библиотеки telebot, random, aiogram.types

    - В файле emphasis.txt хранятся упражнения для ударений в формате абоба Абоба абОба абобА, где Абоба - правильный вариант ответа
    - В файле prepri.txt хранятся упражнения для пре/при в формате пр_абоба Е, преабоба - правильный вариант ответа
    - В файле suffix.txt хранятся упражнения для суффиксов в формате абоб_к И, абобик - правильный вариант ответа
    - В файле prefix.txt хранятся упражнения для приставок в формате д_абоба О, доабоба - правильный вариант ответа
    - В файле users.txt хранится информация о пользователях - их id, имя и счёт.

    - Файл data.py содержит код для поддержания работы с данными пользователей и тренировок

        - Класс User: - пользователь
            - int id - id пользователя
            - str name - имя пользователя
            - int score - счет пользователя
            - int CORRECT_ANSWER_INCREMENT, int INCORRECT_ANSWER_DECREMENT - как изменяется счет при правильном ответе

            - __init__() - создать пользователя. По умолчанию имя каждого пользователя - "Abobus#____", где вместо ____ выбирается  случайное четырехзначное число
            - def correct_answer() - увеличить счет пользователя на CORRECT_ANSWER_INCREMENT
            - def incorrect_answer() - уменьшить счет пользователя на INCORRECT_ANSWER_DECREMENT
            - def write() - записать пользователя в users.txt
            - def reset() - сбросить счет пользователя
            - def rename(str name) - переименовать пользователя

        - Класс UserDatabase: - здесь хранится информация о пользователях 
            - dict users - по id пользователя можно получить информацию о нём
            - User top_user
            - dict wait_list - список пользователей с необработанными запросами
            - dict type - какой статус у пользователя. 0 - ударение, 1 - пре/при, 3 - смена имени, 2 - префикс, 4 - суффикс

            - __init__() - загружаются данные из users.txt
            - def sync_file() - синхронизировать users.txt с текущей информацией о пользователях
            - def update_top() - обновить топ
            - def add_user(int user_id) - добавить пользователя в базу
            - def exists(int user_id) - присутствует ли пользователь в базе
            - def get_score(int user_id) - узнать счет пользователя
            - def reset(int user_id) - сбросить счет пользователя
            - def answered(int user_id, bool status) - обработать ответ пользователя

        - Класс Exercise:
            - str question - вопрос, который выведется 
            - str answer - ожидаемый ответ
            - list variants - варианты ответа 

            - __init__(str question, str answer, list variants)

        - Класс ExercisesList:
            - str type - упражнения какого типа содержит
            - list exercises - список упражнений

            - __init__(str type) - загружает тренировки из соответствующего файла
            - def pick() - выбирает случайную тренировку из списка тренировок

    - Файл main.py содержит основную логику работы бота

        - telebot bot - имеет ключ 6840057545:AAEJ2iaYYdauLkadStHlKOWn6ZihvKGJ-xA

        - UserDatabase users

        - ExercisesList EmphasisExercises
        - ExercisesList PrePriExercises
        - ExercisesList SuffixExercises
        - ExercisesList PrefixExercises

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
