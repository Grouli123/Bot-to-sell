import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime
import time

import re

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

geolocator = None

nuberPhone = None
city = None
lastname = None
firstname = None
middlename = None
dataOfBirth = None       
citizenRF = None

passport = None

user_id = None



cityTrue = False

check_user_id = None




nalogacc = None





editButtonText1 = 'Сбербанк'
editButtonText2 = 'Тинькофф'
editButtonText3 = 'Другой банк'

@bot.message_handler(commands=['start'])
def registration(message):
    global user_id
    global check_user_id
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

    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
          # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки
    
    if takeParam:
        check_user_id = takeParam[9]
    else:
        check_user_id = None
    conn.close()

    if check_user_id is not None or user_id is not None:
        bot.send_message(message.chat.id, f'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажам на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на твоей клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
        userCitizenRuText = f'👉Пока можешь почитать отзывы о нашей организации'
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)  
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)



    
    

@bot.message_handler(commands=['data'])
def data(message):
    global user_id

    global city

    
    global cityTrue


    global nuberPhone
    global city
    global lastname
    global firstname
    global middlename
    global dataOfBirth       
    global citizenRF 

    global check_user_id
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
    
        # Подключение к базе данных SQLite
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()

        # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки
    
    if takeParam:
        check_user_id = takeParam[9]
    else:
        check_user_id = None
    conn.close()
    
    if takeParam:
        nuberPhone = takeParam[2]
        city = takeParam[3]
        lastname = takeParam[4]
        firstname = takeParam[5]
        middlename = takeParam[6]
        dataOfBirth = takeParam[7]        
        citizenRF = takeParam[8]   

    else:
        print('Значение не найдено') # Сообщение, если значение не найдено

        # Закрытие соединения с базой данных
    conn.close()
    if check_user_id is not None or user_id is not None:
        if cityTrue is False:
            markup = types.InlineKeyboardMarkup()
            btn2 = types.InlineKeyboardButton('🖌Редактировать город', callback_data='🖌Редактировать город', one_time_keyboard=True)
            btn3 = types.InlineKeyboardButton('✅Подтвердить', callback_data='✅Подтвердить', one_time_keyboard=True)
            markup.row(btn2)  
            markup.row(btn3)  
            bot.send_message(message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить', reply_markup=markup)
            print('первый иф',check_user_id, 'продолжение', user_id)
        else:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('📝Редактировать данные', callback_data='📝Редактировать данные', one_time_keyboard=True)
            btn2 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='📊 Статистика заказов', one_time_keyboard=True)
            btn3 = types.InlineKeyboardButton('✅Подтвердить аккаунт', callback_data='✅Подтвердить аккаунт', one_time_keyboard=True)
            btn4 = types.InlineKeyboardButton('✅Самозанятость', callback_data='✅Самозанятость', one_time_keyboard=True)
            markup.row(btn1)  
            markup.row(btn2)  
            markup.row(btn3)  
            markup.row(btn4)  
            bot.send_message(message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить', reply_markup=markup)
            print('первый элс',check_user_id, 'продолжение', user_id)
    else:
        print('второй иф',check_user_id, 'продолжение', user_id)
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=['orders'])
def orders(message):

    global check_user_id
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
    
        # Подключение к базе данных SQLite
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()

        # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки
    
    if takeParam:
        check_user_id = takeParam[9]
    else:
        check_user_id = None
    conn.close()
    if check_user_id is not None or user_id is not None:
        usercitizenRF = 'На данный момент у Вас нет активных заявок. Следите за новыми заявками и берите те, по которым хотите работать.'   
        bot.send_message(message.chat.id, usercitizenRF)
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)



def input_birtgday(message):
    bot.send_message(message.chat.id, dataOfBirthday, parse_mode='html')
    bot.register_next_step_handler(message, user_birthday_check)

def get_date(text):
    try:
        date = datetime.strptime(text, dateType)
        return date.strftime(dateType)
    except ValueError:
        return None

def user_birthday_check(message):
    global dataOfBirth    
    try:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_birtgday(message)
        else:
            dataOfBirth = get_date(message.text.strip())
            if dataOfBirth:
                print('OP')
            else:
                bot.send_message(message.chat.id, dateError)
                bot.register_next_step_handler(message, user_birthday_check)
    except ValueError:
        bot.send_message(message.chat.id, dateError)
        bot.register_next_step_handler(message, user_birthday_check)



def input_birtgday2(message):
    bot.send_message(message.chat.id, dataOfBirthday, parse_mode='html')
    bot.register_next_step_handler(message, user_birthday_check2)

def get_date2(text):
    try:
        date = datetime.strptime(text, dateType)
        return date.strftime(dateType)
    except ValueError:
        return None

def user_birthday_check2(message):
    global dataOfBirth    
    try:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_birtgday2(message)
        else:
            dataOfBirth = get_date2(message.text.strip())
            if dataOfBirth:
                print('OP')
            else:
                bot.send_message(message.chat.id, dateError)
                bot.register_next_step_handler(message, user_birthday_check2)
    except ValueError:
        bot.send_message(message.chat.id, dateError)
        bot.register_next_step_handler(message, user_birthday_check2)



@bot.callback_query_handler(func=lambda callback: callback.data == '📝Редактировать данные')
@bot.callback_query_handler(func=lambda callback: callback.data == '📊 Статистика заказов') 
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Подтвердить аккаунт')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Самозанятость')
def callback_data_of_data(callback): 
    global cityTrue
    if callback.data == '📝Редактировать данные':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cityTrue = False
        data(callback.message)

    elif callback.data == '📊 Статистика заказов':        
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.send_message(callback.message.chat.id, f'📊 Статистика заказов:\n• Взял 0\n• Выполнил 0 (0%)\n• Брак 0 (0%)', reply_markup=markup)

    elif callback.data == '✅Подтвердить аккаунт': 
        print(nuberPhone , lastname)
        bot.edit_message_text(f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}', callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        input_lastname(callback.message)   
    elif callback.data == '✅Самозанятость': 
        bot.edit_message_text(f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: Нет \n🏙 Город(а): {city}', callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Кто такой самозанятый❓', callback_data='Кто такой самозанятый❓', one_time_keyboard=True, url='https://npd.nalog.ru/')
        btn2 = types.InlineKeyboardButton('✅Да, официально зарегистрирован', callback_data='✅Да, официально зареган', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('☑️ Нет, хочу зарегистрироваться', callback_data='☑️ Нет, хочу зарегистрироваться', one_time_keyboard=True)
        btn4 = types.InlineKeyboardButton('➡️ Нет, пропустить', callback_data='➡️ Нет, пропустить', one_time_keyboard=True)

        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)  
                
                
        bot.send_message(callback.message.chat.id, f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Да, официально зареган')
@bot.callback_query_handler(func=lambda callback: callback.data == '☑️ Нет, хочу зарегистрироваться')
@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Нет, пропустить')
def callback_individual(callback): 
    global editButtonText1
    global editButtonText2
    global editButtonText3
    

    editButtonText1 = 'Сбербанк'
    editButtonText2 = 'Тинькофф'
    editButtonText3 = 'Другой банк'

    if callback.data == '☑️ Нет, хочу зарегистрироваться':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)        

        markup.row(btn1, btn2, btn3)

        bot.send_message(callback.message.chat.id, f'🏦 Каким банком пользуешься?', reply_markup=markup)

    elif callback.data == '➡️ Нет, пропустить':
        bot.edit_message_text(f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', callback.message.chat.id, callback.message.message_id)
    elif callback.data == '✅Да, официально зареган':
        input_my_nalog_accaunt(callback.message)


def input_my_nalog_accaunt(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('➡️ Пропустить', callback_data='➡️ Пропустить2', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, 'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, my_nalog_accaunt_check)   

def my_nalog_accaunt_check(message):
    global nalogacc
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_my_nalog_accaunt(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_my_nalog_accaunt(message) 
        else:
            nalogacc = message.text.strip()
            print(nalogacc)


@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Пропустить2')
def callback_bank(callback):
    if callback.data == '➡️ Пропустить2': 
        bot.edit_message_text(f'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', callback.message.chat.id, callback.message.message_id)
        data(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText1)
@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText2)
@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText3)
def callback_bank(callback): 
    
    global editButtonText1
    global editButtonText2
    global editButtonText3
    if callback.data == editButtonText1:
        editButtonText1 = '✅ Сбербанк'
        editButtonText2 = 'Тинькофф'
        editButtonText3 = 'Другой банк'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)  
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)        

        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'В приложении СберБанк Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)   
    elif callback.data == editButtonText2:
        editButtonText2 = '✅Тинькофф'        
        editButtonText1 = 'Сбербанк'
        editButtonText3 = 'Другой банк'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)        
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)     

        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'В приложении Тинькофф Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == editButtonText3:
        editButtonText3 = '✅Другой банк'
        editButtonText1 = 'Сбербанк'
        editButtonText2 = 'Тинькофф'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True) 
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)            

        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'В приложении Другой банк Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
   


@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Продолжить')
def callback_edit_data_person(callback): 
    if callback.data == '➡️ Продолжить':
        bot.send_message(callback.message.chat.id, f'Сначала необходимо подтвердить паспортные данные!', parse_mode='html')

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🖌Редактировать ФИО', callback_data='🖌Редактировать ФИО', one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton('🖌Редактировать дату рождения',callback_data='🖌Редактировать ДР', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('🖌Редактировать паспорт', callback_data='🖌Редактировать ПС', one_time_keyboard=True)        
        btn4 = types.InlineKeyboardButton('✅ Подтвердить(Осталось попыток:2)', callback_data='✅ Подтвердить', one_time_keyboard=True)
        btn5 = types.InlineKeyboardButton('➡️ Пропустить, остаться с низким приоритетом', callback_data='➡️ Пропустить', one_time_keyboard=True)

        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)
        markup.row(btn5)
        bot.send_message(callback.message.chat.id, f'ФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ФИО')
@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ДР')
@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ПС')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅ Подтвердить')
@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Пропустить')
def callback_edit_person_data_alone(callback): 
    if callback.data == '🖌Редактировать ФИО':
        input_lastname2(callback.message)
    elif callback.data == '🖌Редактировать ДР':
        user_birthday_check2(callback.message)
    elif callback.data == '🖌Редактировать ПС':
        input_passport(callback.message)
    elif callback.data == '✅ Подтвердить':
        bot.answer_callback_query(callback_query_id=callback.id, text='Аккаунт подтвержден')        
        bot.edit_message_text(f'ФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', callback.message.chat.id, callback.message.message_id)

    elif callback.data == '➡️ Пропустить':
        bot.edit_message_text(f'ФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', callback.message.chat.id, callback.message.message_id)


def input_lastname2(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, 'Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, lastneme_check2)   

def lastneme_check2(message):
    global lastname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_lastname2(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_lastname2(message) 
        else:
            lastname = message.text.strip()
            print(lastname)
            input_firstname2(message)


def input_firstname2(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО имя как в паспорте:', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, firstname_check2)

def firstname_check2(message):       
    global firstname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_firstname2(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_firstname2(message)        
        else:                  
            firstname = message.text.strip()    
            print(firstname_check)
            input_middlename2(message)
        
def input_middlename2(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО отчество как в паспорте:', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, middlename_check2)

def middlename_check2(message):      
    global middlename
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_middlename2(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, middlenameError)
            message.text.strip(None)
            input_middlename2(message) 
        else:     
            middlename = message.text.strip()
            print(middlename_check)





@bot.callback_query_handler(func=lambda callback: callback.data == '❌ Отменить подтверждение')
def callback_delete_previos_message(callback): 
    if callback.data == '❌ Отменить подтверждение':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        data(callback.message)


def input_lastname(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, 'Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', parse_mode='html', reply_markup=markup)
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
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО имя как в паспорте:', parse_mode='html', reply_markup=markup)
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
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО отчество как в паспорте:', parse_mode='html', reply_markup=markup)
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
            input_passport(message)


def input_passport(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, 'ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXX YYYYYY, где XXXX - серия, YYYYYY - номер.', parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda message: bool(re.match(r'^\d{4} \d{6}$', message.text))) 
def passport_check(message):      
    global passport    
    passport = message.text.strip()
    print(passport)
    readyPassportInfo(message)

@bot.message_handler(func=lambda message: True) 
def passport_check(message):      
    bot.send_message(message.chat.id, 'Введите цифры', parse_mode='html')
    input_passport(message)


def readyPassportInfo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🖌Редактировать ФИО', callback_data='🖌Редактировать ФИО', one_time_keyboard=True)
    btn2 = types.InlineKeyboardButton('🖌Редактировать дату рождения',callback_data='🖌Редактировать ДР', one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton('🖌Редактировать паспорт', callback_data='🖌Редактировать ПС', one_time_keyboard=True)        
    btn4 = types.InlineKeyboardButton('✅ Подтвердить(Осталось попыток:2)', callback_data='✅ Подтвердить', one_time_keyboard=True)
    btn5 = types.InlineKeyboardButton('➡️ Пропустить, остаться с низким приоритетом', callback_data='➡️ Пропустить', one_time_keyboard=True)

    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)
    markup.row(btn5)
    bot.send_message(message.chat.id, f'Введите верные данные паспорта (фио/дата рождения/серия+номер)\n\nФИО: {lastname} {firstname} {middlename}\n\nДата рождения: {dataOfBirth}\n\nСерия и номер паспорта: {passport}', parse_mode='html', reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать город')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Подтвердить') 
def callback_rename_city(callback): 
    global cityTrue
  
    if callback.data == '🖌Редактировать город':
        usercitizenRF = f'Выбрано: 🟢{city}'        
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(f'❌Удалить "{city}"', callback_data=f'❌Удалить "{city}"', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('✅Продолжить', callback_data='✅Продолжить', one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.edit_message_text(usercitizenRF, callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    elif callback.data == '✅Подтвердить':
        cityTrue = True
        bot.edit_message_text('Данные успешно обновлены!', callback.message.chat.id, callback.message.message_id)
        data(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == f'❌Удалить "{city}"')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Продолжить') 
def callback_delete_city(callback):   
    if callback.data == f'❌Удалить "{city}"':
        markup = types.InlineKeyboardMarkup()
        btn3 = types.InlineKeyboardButton('✅Добавить город', callback_data='✅Добавить город', one_time_keyboard=True) 
        markup.row(btn3)  
        bot.edit_message_text('Укажи город, где хочешь работать.', callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Добавить город') 
def callback_add_city(callback):   
    if callback.data == '✅Добавить город':
        locationCityCitizen(callback.message)        

    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)


def locationCityCitizen(message):
    try:
        global geolocator
        keyboard = types.ReplyKeyboardMarkup()
        button_geo = types.KeyboardButton(text=geolocationButtonText, request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, '⚠️Включи геолокацию на телефоне!⚠️\n\nОтправь свой город👇👇👇\n\nℹ️ Определение города может занять некоторое время🕰.', reply_markup=keyboard)  

        bot.register_next_step_handler(message, location)
        geolocator = Nominatim(user_agent = geolocationNameApp)    
    except Exception:        
        bot.send_message(message.chat.id, phoneError, parse_mode='html')
        bot.register_next_step_handler(message, locationCityCitizen)   

def city_check(coord):
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address'] 
    town = address.get('town', '')
    city = address.get('city', '')
    if town == '':
        town = city
    if city == '':
        city = town  

    return city

def location(message):
    global locationcity
    if message.location is not None:           
        a = [message.location.latitude, message.location.longitude]         
        city_name = city_check(a)
        locationcity = city_name
        bot.send_message(message.chat.id, f'{foundedCity} {locationcity}', reply_markup=types.ReplyKeyboardRemove())
        
        markup = types.InlineKeyboardMarkup()
        btn3 = types.InlineKeyboardButton('✅Продолжить', callback_data='✅Продолжить2', one_time_keyboard=True) 
        markup.row(btn3)  
        bot.send_message(message.chat.id, f'На данный момент нельзя изменить город. Такая возможность будет через 13 дней.\nВыбрано: 🟢{city}', reply_markup=markup)            
    else:        
        bot.send_message(message.chat.id, geolocationError, parse_mode='html')
        bot.register_next_step_handler(message, location)   


@bot.callback_query_handler(func=lambda callback: callback.data == '✅Продолжить2') 
def callback_message_citizen(callback):   
    if callback.data == '✅Продолжить2':
        bot.answer_callback_query(callback_query_id=callback.id, text='Сначала нужно завершить редактирование данных. Чтобы завершить нажмите ✅Подтвердить',show_alert=True)
        data(callback.message)
    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)


if __name__ == '__main__':
    print('Bot started')
    bot.polling(non_stop=True)
