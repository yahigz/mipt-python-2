import sys 

import telebot
from telebot import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sys.path.append("./src")

from data import *

bot = telebot.TeleBot('6840057545:AAEJ2iaYYdauLkadStHlKOWn6ZihvKGJ-xA')

EmphasisExercises = ExercisesList("emphasis")
PrePriExercises = ExercisesList("prepri")
SuffixExercises = ExercisesList("suffix")
PrefixExercises = ExercisesList("prefix")
Users = UserDatabase()
#глобальные переменные :( но не понятно как тут без них

@bot.message_handler(commands=["start"])
def start(message, res=False):
    if not Users.exists(message.chat.id):
        Users.add_user(message.chat.id)

    bot.send_message(message.chat.id, "Меню /start\nПре-/При- /prepri\nСуффиксы /suffix\nПриставки /prefix\nУдарения /emphasis\nСчет /score\nТоп-1 /top\nСбросить очки /reset\nСменить имя /rename")

@bot.message_handler(commands=["score"])
def score(message, res=False):
    bot.send_message(message.chat.id, "Ваш счет: " + str(Users.get_score(message.chat.id)))

@bot.message_handler(commands=["top"])
def top(message, res=False):
    Users.update_top()
    bot.send_message(message.chat.id, "Топ-1: " + str(Users.top_user.name) + ' с ' + str(Users.top_user.score) + ' очками')

@bot.message_handler(commands=["reset"])
def reset(message, res=False):
    Users.reset(message.chat.id)
    bot.send_message(message.chat.id, "Ваш счет сброшен")

@bot.message_handler(commands=["prepri"])
def prepri(message, res=False):
    exercise = PrePriExercises.pick()
    Users.wait_list[message.chat.id] = exercise
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Users.type[message.chat.id] = 1

    buttons = []
    for variant in exercise.variants:
        buttons.append(types.KeyboardButton(str(variant)))
                      
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, '❓Выберите правильное написание: ' + str(exercise.question), reply_markup=keyboard)

@bot.message_handler(commands=["prefix"])
def prefix(message, res=False):
    exercise = PrefixExercises.pick()
    Users.wait_list[message.chat.id] = exercise
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Users.type[message.chat.id] = 2

    buttons = []
    for variant in exercise.variants:
        buttons.append(types.KeyboardButton(str(variant)))
                      
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, '❓Выберите правильное написание: ' + str(exercise.question), reply_markup=keyboard)

@bot.message_handler(commands=["suffix"])
def suffix(message, res=False):
    exercise = SuffixExercises.pick()
    Users.wait_list[message.chat.id] = exercise
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Users.type[message.chat.id] = 4

    buttons = []
    for variant in exercise.variants:
        buttons.append(types.KeyboardButton(str(variant)))
                      
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, '❓Выберите правильное написание: ' + str(exercise.question), reply_markup=keyboard)

@bot.message_handler(commands=["emphasis"])
def emphasis(message, res=False):
    exercise = EmphasisExercises.pick()
    Users.wait_list[message.chat.id] = exercise
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Users.type[message.chat.id] = 0

    buttons = []
    for variant in exercise.variants:
        buttons.append(types.KeyboardButton(str(variant)))
                      
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, '❓Выберите правильное ударение: ' + str(exercise.question), reply_markup=keyboard)

@bot.message_handler(commands=["rename"])
def rename(message, res=False):
    if not Users.exists(message.chat.id):
        Users.add_user(message.chat.id)
    
    Users.type[message.chat.id] = 3
    Users.wait_list[message.chat.id] = None
    bot.send_message(message.chat.id, 'Введите новое имя:')

@bot.message_handler(commands=["sync_file_z9bmiMjuK9wFyEXOCBFMzVwqBAAlDdt8"])
def sync(message, res=False):
    Users.sync_file()
    bot.send_message(message.chat.id, 'Синхронизация выполнена')

@bot.message_handler(content_types=["text"])
def checker(message):
    print(message.text + ' ' + str(Users.users[message.chat.id].name))
    if message.chat.id in Users.wait_list and Users.type[message.chat.id] == 3:
        Users.rename(message.chat.id, str(message.text))
        bot.send_message(message.chat.id, 'Новое имя установлено: ' + message.text)
        return
    
    if message.chat.id in Users.wait_list:
        if message.text.strip() == Users.wait_list[message.chat.id].answer:
            Users.answered(message.chat.id, True)
            bot.send_message(message.chat.id, "✅Верно")
        else:
            Users.answered(message.chat.id, False)
            if Users.type[message.chat.id] != 0:
                bot.send_message(message.chat.id, "❌Ошибка, правильно: " + Users.wait_list[message.chat.id].question.replace("_", Users.wait_list[message.chat.id].answer))
            else:
                bot.send_message(message.chat.id, "❌Ошибка, правильно: " + Users.wait_list[message.chat.id].answer)    
        
        if Users.type[message.chat.id] == 1:
            prepri(message)
        
        if Users.type[message.chat.id] == 0:
            emphasis(message)

        if Users.type[message.chat.id] == 4:
            suffix(message)
        
        if Users.type[message.chat.id] == 2:
            prefix(message)
    else:
        start(message)    

if (__name__ == '__main__'):    
    bot.polling(none_stop=True, interval=0)