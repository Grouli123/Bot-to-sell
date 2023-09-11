import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter
from telebot import types

import APIbot

botApiKey = APIbot.botApi
bot = telebot.TeleBot(botApiKey)

cityObject = None
countPeople = None
aressOfObject = None
whatToDo = None
startOfWork = None
salary = None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Сформировать заявку')
    btn2 = types.KeyboardButton('Открыть базу данных')
    markup.row(btn1, btn2)    
    bot.send_message(message.chat.id, 'Рад помочь, выберите подходящий пункт',  reply_markup=markup)
    bot.register_next_step_handler(message, city_of_obj)

def city_of_obj(message):
    if message.text == 'Сформировать заявку':
        bot.send_message(message.chat.id, "Напишите город объекта: ")
        bot.register_next_step_handler(message, city_of_obj_check)

    elif message.text == 'Открыть базу данных':
        bot.send_message(message.chat.id, "Скоро разработаем")

def city_of_obj_check(message):
    global cityObject
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_count_people(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_count_people(message) 
        else:
            cityObject = message.text.strip()
            print(cityObject)
            input_count_people(message)

def input_count_people(message):
    bot.send_message(message.chat.id, 'Напишите количество требуемых рабочих:  ', parse_mode='html')
    bot.register_next_step_handler(message, count_people_check) 

def count_people_check(message):
    global countPeople
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_count_people(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_count_people(message) 
        else:
            countPeople = message.text.strip()
            print(countPeople)
            input_adress(message)

def input_adress(message):
    bot.send_message(message.chat.id, 'Напишите адрес объекта: ', parse_mode='html')
    bot.register_next_step_handler(message, agress_check) 

def agress_check(message):
    global aressOfObject
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_adress(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_adress(message) 
        else:
            aressOfObject = message.text.strip()
            print(aressOfObject)
            input_to_do(message)


def input_to_do(message):
    bot.send_message(message.chat.id, 'Напишите что нужно делать: ', parse_mode='html')
    bot.register_next_step_handler(message, to_do_check) 

def to_do_check(message):
    global whatToDo
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_to_do(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_to_do(message) 
        else:
            whatToDo = message.text.strip()
            print(whatToDo)
            input_start_work(message)

def input_start_work(message):
    bot.send_message(message.chat.id, 'Напишите начало работы: ', parse_mode='html')
    bot.register_next_step_handler(message, start_work_check) 

def start_work_check(message):
    global startOfWork
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_start_work(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_start_work(message) 
        else:
            startOfWork = message.text.strip()
            print(startOfWork)
            input_salary(message)


def input_salary(message):
    bot.send_message(message.chat.id, 'Напишите зарплату и минимальное время: ', parse_mode='html')
    bot.register_next_step_handler(message, start_work_check) 

def salary_check(message):
    global salary
    if message.text is None:
        bot.send_message(message.from_user.id, 'Ошибка, сообщение должно быть текстом')
        input_salary(message) 
    else:
        if len(message.text.strip()) > 50:
            bot.send_message(message.chat.id, 'Слишком большое количество символов')
            message.text.strip(None)
            input_salary(message) 
        else:
            salary = message.text.strip()
            print(salary)
            citizenRU(message)

def citizenRU(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Да', callback_data='Да', one_time_keyboard=True)
    # btn3 = types.InlineKeyboardButton('', callback_data='', one_time_keyboard=True)
    markup.row(btn2)    
    bot.send_message(message.chat.id, 'Хотете посмотреть заявку?', reply_markup=markup)  

# @bot.callback_query_handler(func=lambda callback: callback.data == '')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Да') 
def callback_message_citizen(callback):   
    # global usercitizenRF 
    if callback.data == 'Да':
        # usercitizenRF = ''        
        bot.edit_message_text('Да', callback.message.chat.id, callback.message.message_id)    
        bot.send_message(callback.message.chat.id, f'✅\n<b>·{cityObject}:</b> {countPeople}\n<b>·Адрес:</b>👉{aressOfObject}\n<b>·Что делать:</b> {whatToDo}\n<b>·Начало работ:</b> {startOfWork}\n<b>·Вам на руки:</b> {salary}\n<b>·Приоритет самозанятым</b>', parse_mode='html')

    else:          
        # usercitizenRF = ''
        bot.edit_message_text('', callback.message.chat.id, callback.message.message_id)
    
    # bot.send_message(callback.message.chat.id, f'✅\n<b>·{cityObject}:</b> {countPeople}\n<b>·Адрес:</b>👉{aressOfObject}\n<b>·Что делать:</b> {whatToDo}\n<b>·Начало работ:</b> {startOfWork}\n<b>·Вам на руки:</b> {salary}\n<b>·Приоритет самозанятым</b>', parse_mode='html')
    # import_into_database(callback.message)

# def import_into_database(message):
#     global usercitizenRF   
#     global state  
#     conn = sqlite3.connect('./peoplebase.sql')
#     cur = conn.cursor()
#     cur.execute(insertIntoBase % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF)) 
   
#     conn.commit()
#     cur.close()
#     conn.close()
    

#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton(f'{buttonResultName} {cityname}', callback_data=nameOfBase))
       
#     bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
#     state = 'citizenRU'

# @bot.callback_query_handler(func=lambda call: call.data == nameOfBase)
# def show_database(call):
#     conn = sqlite3.connect('./peoplebase.sql')
#     cur = conn.cursor()

#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()

#     info = ''
#     for el in users:
#         info += f'Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n'

#     cur.close()
#     conn.close()

#     bot.send_message(call.message.chat.id, info)
#     print(info)

print('Bot started')


bot.polling(non_stop=True)