import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime

import API_key
import sqlBase as sqlBase
import config_message

botApiKey = API_key.botAPI

bot = telebot.TeleBot(botApiKey)

base = sqlBase.createDatabase
insertIntoBase = sqlBase.insertIntoDatabase
nameOfBase = sqlBase.name_of_base

maxSymbol = config_message.max_symbol_for_message

lastnameText = config_message.input_lastname_text
lastnameError = config_message.lastname_error

firstnameText = config_message.input_firstname_text
firstnameError = config_message.firstname_error

middlenameText = config_message.input_middlename_text
middlenameError = config_message.middlename_error

textOnly = config_message.message_should_be_text_type

citizenRuButtonYesText = config_message.citizen_ru_button_yes
citizenRuButtonYesTextCallbackData = config_message.citizen_ru_button_yes_callback_data

citizenRuButtonNoText = config_message.citizen_ru_button_no
citizenRuButtonNoTextCallbackData = config_message.citizen_ru_button_no_callback_data

userCitizenRuText = config_message.user_citizen_ru_text
userCitizenRuError = config_message.user_citizen_ru_error

registrationSucsess = config_message.registration_sucsess
buttonResultName = config_message.button_result_name

alreadyRegistered = config_message.already_registered

phone = None
lastname = None
firstname = None
middlename = None
userbirthday = None

usercitizenRF = None

locationcity = None

cityname = None

countPeople = None

state = 'initial'

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
        bot.send_message(message.chat.id, "Напишите город объекта: ", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, city_of_obj_check)

    elif message.text == 'Открыть базу данных':
        bot.send_message(message.chat.id, 'Вот база данных пользователей: ')
        show_database(message)
        # start(message)

def city_of_obj_check(message):
    global cityname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        city_of_obj(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            city_of_obj(message) 
        else:
            cityname = message.text.strip()
            print(cityname)
            registration(message)

def registration(message):
    conn = sqlite3.connect('./applicationbase.sql')
    cur = conn.cursor()

    cur.execute(base)
    conn.commit() 
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Напишите количество требуемых рабочих: ', parse_mode='html')
    bot.register_next_step_handler(message, registration_check)   

def registration_check(message):
    global countPeople
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        registration(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            registration(message) 
        else:
            countPeople = message.text.strip()
            print(countPeople)
            input_lastname(message)
        
def input_lastname(message):
    bot.send_message(message.chat.id, lastnameText, parse_mode='html')
    bot.register_next_step_handler(message, lastneme_check)   

def lastneme_check(message):
    global lastname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_lastname(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_lastname(message) 
        else:
            lastname = message.text.strip()
            print(lastname)
            input_firstname(message)

def input_firstname(message):
    bot.send_message(message.chat.id, firstnameText, parse_mode='html')
    bot.register_next_step_handler(message, firstname_check)

def firstname_check(message):       
    global firstname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_firstname(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_firstname(message)        
        else:                  
            firstname = message.text.strip()    
            print(firstname_check)
            input_middlename(message)
        
def input_middlename(message):
    bot.send_message(message.chat.id, middlenameText, parse_mode='html')
    bot.register_next_step_handler(message, middlename_check)

def middlename_check(message):      
    global middlename
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_middlename(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, middlenameError)
            message.text.strip(None)
            input_middlename(message) 
        else:     
            middlename = message.text.strip()
            print(middlename_check)
            input_middlenam2(message)

def input_middlenam2(message):
    bot.send_message(message.chat.id, 'Напишите зарплату и минимальное время: ', parse_mode='html')
    bot.register_next_step_handler(message, input_middlenam2_check)

def input_middlenam2_check(message):      
    global salary
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_middlenam2(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, middlenameError)
            message.text.strip(None)
            input_middlenam2(message) 
        else:     
            salary = message.text.strip()
            print(middlename_check)
            citizenRU(message)

def citizenRU(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b> {countPeople}\n<b>·Адрес:</b>👉{lastname}\n<b>·Что делать:</b> {firstname}\n<b>·Начало работ:</b> {middlename}\n<b>·Вам на руки:</b> {salary}\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    # bot.forward_message('6489313384', '6672528914', message.message_id-1)
    start(message)

@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonYesTextCallbackData)
@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonNoTextCallbackData) 
def callback_message_citizen(callback):   
    global usercitizenRF 
    if callback.data == citizenRuButtonYesTextCallbackData:
        usercitizenRF = citizenRuButtonYesText        
        bot.edit_message_text(f'{userCitizenRuText}\n\n✅\n<b>·{cityname}: </b> {countPeople}\n<b>·Адрес:</b>👉{lastname}\n<b>·Что делать:</b> {firstname}\n<b>·Начало работ:</b> {middlename}\n<b>·Вам на руки:</b> {salary}\n<b>·Приоритет самозанятым</b>', callback.message.chat.id, callback.message.message_id, parse_mode='html')
        

    else:          
        usercitizenRF = citizenRuButtonNoText
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    import_into_database(callback.message)

@bot.message_handler(content_types=['text'])
def check_callback_message_citizen(message):          
        global state      
        if state == 'initial':         
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            citizenRU(message)         
        elif state == 'citizenRU':
            bot.send_message(message.chat.id, registrationSucsess, parse_mode='html')
            import_into_database(message)
        else:
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id)

def import_into_database(message):
    global usercitizenRF   
    global state  
    conn = sqlite3.connect('./applicationbase.sql')
    cur = conn.cursor()
    cur.execute(insertIntoBase % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF)) 
   
    conn.commit()
    cur.close()
    conn.close()
    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {cityname}', url='https://t.me/ArJobBot'))
       
    bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    state = 'citizenRU'

def show_database(message):
    conn = sqlite3.connect('./peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n'

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)
    print(info)

print('Bot started')

bot.polling(non_stop=True)