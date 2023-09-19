import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime
import time

import  get_orders_config.get_orders_API_key as API_key
import get_orders_config.get_orders_sqlBase as sqlBase
import  get_orders_config.get_orders_config_message as config_message


botApiKey = API_key.botAPI

bot = telebot.TeleBot(botApiKey)

base = sqlBase.createDatabase
insertIntoBase = sqlBase.insertIntoDatabase
nameOfBase = sqlBase.name_of_base

maxSymbol = config_message.max_symbol_for_message

phoneButtonText = config_message.phone_button_text
phoneMessageText = config_message.message_to_send_phonenumber
phoneError = config_message.phone_error

geolocationButtonText = config_message.geolocation_button_text
geolocationMessageText = config_message.message_to_send_geolocation
geolocationNameApp = config_message.geolocator_name_app
foundedCity = config_message.founded_city
geolocationError = config_message.geolocation_error

lastnameText = config_message.input_lastname_text
lastnameError = config_message.lastname_error

firstnameText = config_message.input_firstname_text
firstnameError = config_message.firstname_error

middlenameText = config_message.input_middlename_text
middlenameError = config_message.middlename_error

dataOfBirthday = config_message.input_bitrhday_data_text
dateType = config_message.date_type
dateError = config_message.date_error

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

# phone = None
# lastname = None
# firstname = None
# middlename = None
# userbirthday = None
# usercitizenRF = None
# locationcity = None

# state = 'initial'

# previosMaxValue = 0

# max_id = 0

nuberPhone = None
city = None
lastname = None
firstname = None
middlename = None
dataOfBirth = None       
citizenRF = None

user_id = None

@bot.message_handler(commands=['start'])
def registration(message):
    global user_id
    # global my_variable
    bot.send_message(message.chat.id, f'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажам на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на твоей клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
    userCitizenRuText = f'👉Пока можешь почитать отзывы о нашей организации'
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
    markup.row(btn2)  
    markup.row(btn3)  
    bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)  
    
    conn = sqlite3.connect('user_data.sql')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
    (user_id INTEGER PRIMARY KEY, username TEXT)''')
    conn.commit()
    
    user_id = message.from_user.id
    username = message.from_user.username
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES ('%s', '%s')" % (user_id, username))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['data'])
def data(message):
    global user_id

    global city

    # Подключение к базе данных SQLite
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()

    # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки

    if takeParam:
        nuberPhone = takeParam[2]
        city = takeParam[3]
        lastname = takeParam[4]
        firstname = takeParam[5]
        middlename = takeParam[6]
        dataOfBirth = takeParam[7]        
        citizenRF = takeParam[8]   

        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('🖌Редактировать город', callback_data='🖌Редактировать город', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('✅Подтвердить', callback_data='✅Подтвердить', one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.send_message(message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить', reply_markup=markup)

    else:
        print('Значение не найдено') # Сообщение, если значение не найдено

    # Закрытие соединения с базой данных
    conn.close()


# @bot.message_handler(commands=['orders'])
# def orders(message):
#     bot.send_message(message.chat.id, f'Тут будут ваши заявки', parse_mode='html')

@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать город')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Подтвердить') 
def callback_message_citizen(callback):   
    if callback.data == '🖌Редактировать город':
        usercitizenRF = f'Выбрано: 🟢{city}'        
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(f'❌Удалить "{city}"', callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('✅Продолжить', callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.edit_message_text(usercitizenRF, callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    else:          
        usercitizenRF = 'Пока не робит'
        # bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    
        # bot.send_message(callback.message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить')
    # import_into_database(callback.message)


print('Bot started')

bot.polling(non_stop=True)
