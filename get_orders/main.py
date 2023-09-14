import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime
import time

# import main


import  API_key
import sqlBase as sqlBase
import config_message

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

phone = None
lastname = None
firstname = None
middlename = None
userbirthday = None
usercitizenRF = None
locationcity = None

state = 'initial'

previosMaxValue = 0

max_id = 0

@bot.message_handler(commands=['start'])
def registration(message):
    global previosMaxValue
    
    global max_id

    bot.send_message(message.chat.id, f'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажам на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на твоей клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
    userCitizenRuText = f'👉Пока можешь почитать отзывы о нашей организации'
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
    markup.row(btn2)  
    markup.row(btn3)  
    bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)  
    conn = sqlite3.connect('./peoplebase.sql')
    cur = conn.cursor()
    
    cur.execute(base)
    conn.commit() 
    cur.close()
    conn.close()

    while True:
        # Ожидание определенного интервала времени
        time.sleep(20)

        # Проверка наличия новых записей в базе данных
        
        conn = sqlite3.connect('./applicationbase.sql')
        cur = conn.cursor()
    
        cur.execute('SELECT max(id) FROM orders')

        max_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if max_id != previosMaxValue:
            print("вот: ",max_id)

            conn = sqlite3.connect('./applicationbase.sql')
            cur = conn.cursor()
            # SELECT * FROM users ORDER BY id DESC LIMIT для вывода последнего пользователя
            cur.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 1')
            users = cur.fetchall()

            info = ''
            for el in users:
                info += f'✅\n<b>·{el[2]}:</b> {el[3]}\n<b>·Адрес:</b>👉{el[4]}\n<b>·Что делать:</b> {el[5]}\n<b>·Начало работ:</b> {el[6]}\n<b>·Вам на руки: </b>{el[7]}\n<b>·Приоритет самозанятым</b>'
                # print("вот: ",type(el[0]))
            cur.close()
            conn.close()


            markup2 = types.InlineKeyboardMarkup()
            btn12 = types.InlineKeyboardButton('Еду 1', callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
            btn22 = types.InlineKeyboardButton('Едем в 2', callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
            btn32 = types.InlineKeyboardButton('Едем в 3', callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
            btn42 = types.InlineKeyboardButton('Едем в 4', callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
            btn52 = types.InlineKeyboardButton('❓ Задать вопрос', callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
            markup2.row(btn12)  
            markup2.row(btn22)  
            markup2.row(btn32)  
            markup2.row(btn42)  
            markup2.row(btn52)  
            bot.send_message(message.chat.id, info, parse_mode='html',reply_markup=markup2)  
            # bot.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b> {countPeople}\n<b>·Адрес:</b>👉{adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> {salary}\n<b>·Приоритет самозанятым</b>', parse_mode='html')  

            print(info)

            previosMaxValue = max_id
        elif previosMaxValue == 0:
            print('значение базы равно 0')

        else:
            print('Значение не изменилось')
    # def __init__(self):
    #     global max_id
    #     self._my_var = max_id
 
    # @property
    # def my_var(self):
    #     return self._my_var
    
    # @my_var.setter
    # def my_var(self, value):
    #     if value != self._my_var:
    #         # Выполняем действия при изменении переменной
    #         self._my_var = value
            
    #         print(f"Переменная my_var изменилась с {self._my_var} на {value}")
    #         registration(self._my_var)


    # conn.commit()
    # cur.close()
    # conn.close()
            # Проверка наличия новых записей в базе данных
            
    
    # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
    # keyboard.add(button_phone)
    # bot.send_message(message.chat.id, phoneMessageText, reply_markup=keyboard, parse_mode='html')
    # bot.register_next_step_handler(message, geolocation)   




print('Bot started')

bot.polling(non_stop=True)
# def geolocation(message):    
#     global phone
#     try:
#         phone = message.contact.phone_number
#         global geolocator
#         keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#         button_geo = types.KeyboardButton(text=geolocationButtonText, request_location=True)
#         keyboard.add(button_geo)
#         bot.send_message(message.chat.id, geolocationMessageText, reply_markup=keyboard)
#         bot.register_next_step_handler(message, location)
#         geolocator = Nominatim(user_agent = geolocationNameApp)    
#     except Exception:        
#         bot.send_message(message.chat.id, phoneError, parse_mode='html')
#         bot.register_next_step_handler(message, geolocation)   

# def city_check(coord):
#     location = geolocator.reverse(coord, exactly_one=True)
#     address = location.raw['address'] 
#     town = address.get('town', '')
#     city = address.get('city', '')
#     if town == '':
#         town = city
#     if city == '':
#         city = town  

#     return city

# def location(message):
#     global locationcity
#     if message.location is not None:           
#         a = [message.location.latitude, message.location.longitude]         
#         city_name = city_check(a)
#         locationcity = city_name
#         bot.send_message(message.chat.id, f'{foundedCity} {locationcity}', reply_markup=types.ReplyKeyboardRemove())

#         input_lastname(message)   
            
#     else:        
#         bot.send_message(message.chat.id, geolocationError, parse_mode='html')
#         bot.register_next_step_handler(message, location)   
        
# def input_lastname(message):
#     bot.send_message(message.chat.id, lastnameText, parse_mode='html')
#     bot.register_next_step_handler(message, lastneme_check)   

# def lastneme_check(message):
#     global lastname
#     if message.text is None:
#         bot.send_message(message.from_user.id, textOnly)
#         input_lastname(message) 
#     else:
#         if len(message.text.strip()) > maxSymbol:
#             bot.send_message(message.chat.id, lastnameError)
#             message.text.strip(None)
#             input_lastname(message) 
#         else:
#             lastname = message.text.strip()
#             print(lastname)
#             input_firstname(message)

# def input_firstname(message):
#     bot.send_message(message.chat.id, firstnameText, parse_mode='html')
#     bot.register_next_step_handler(message, firstname_check)

# def firstname_check(message):       
#     global firstname
#     if message.text is None:
#         bot.send_message(message.from_user.id, textOnly)
#         input_firstname(message)
#     else:
#         if len(message.text.strip()) > maxSymbol:
#             bot.send_message(message.chat.id, firstnameError)
#             message.text.strip(None)
#             input_firstname(message)        
#         else:                  
#             firstname = message.text.strip()    
#             print(firstname_check)
#             input_middlename(message)
        
# def input_middlename(message):
#     bot.send_message(message.chat.id, middlenameText, parse_mode='html')
#     bot.register_next_step_handler(message, middlename_check)

# def middlename_check(message):      
#     global middlename
#     if message.text is None:
#         bot.send_message(message.from_user.id, textOnly)
#         input_middlename(message)
#     else:
#         if len(message.text.strip()) > maxSymbol:
#             bot.send_message(message.chat.id, middlenameError)
#             message.text.strip(None)
#             input_middlename(message) 
#         else:     
#             middlename = message.text.strip()
#             print(middlename_check)
#             input_birtgday(message)

# def input_birtgday(message):
#     bot.send_message(message.chat.id, dataOfBirthday, parse_mode='html')
#     bot.register_next_step_handler(message, user_birthday_check)

# def get_date(text):
#     try:
#         date = datetime.strptime(text, dateType)
#         return date.strftime(dateType)
#     except ValueError:
#         return None

# def user_birthday_check(message):
#     global userbirthday    
#     try:
#         if message.text is None:
#             bot.send_message(message.from_user.id, textOnly)
#             input_birtgday(message)
#         else:
#             userbirthday = get_date(message.text.strip())
#             if userbirthday:
#                 citizenRU(message)
#             else:
#                 bot.send_message(message.chat.id, dateError)
#                 bot.register_next_step_handler(message, user_birthday_check)
#     except ValueError:
#         bot.send_message(message.chat.id, dateError)
#         bot.register_next_step_handler(message, user_birthday_check)

# def citizenRU(message):
#     markup = types.InlineKeyboardMarkup()
#     btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
#     btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
#     markup.row(btn2, btn3)    
#     bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)  

# @bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonYesTextCallbackData)
# @bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonNoTextCallbackData) 
# def callback_message_citizen(callback):   
#     global usercitizenRF 
#     if callback.data == citizenRuButtonYesTextCallbackData:
#         usercitizenRF = citizenRuButtonYesText        
#         bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
#     else:          
#         usercitizenRF = citizenRuButtonNoText
#         bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    
#     bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: {usercitizenRF}\n🏙 Город(а): {locationcity}')
#     import_into_database(callback.message)

# @bot.message_handler(content_types=['text'])
# def check_callback_message_citizen(message):          
#         global state      
#         if state == 'initial':         
#             bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
#             bot.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
#             citizenRU(message)         
#         elif state == 'citizenRU':
#             bot.send_message(message.chat.id, registrationSucsess, parse_mode='html')
#             import_into_database(message)
#         else:
#             bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id)

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
#     markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBase, url='https://t.me/ArJobBot'))
       
#     bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
#     state = 'citizenRU'

