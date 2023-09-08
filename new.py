import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from geopy.geocoders import Nominatim
import time

# import config
from datetime import datetime
from dateutil.parser import parse

bot = telebot.TeleBot('6484701618:AAFcxH0T31Rl_XakKMfFm5PWsLwSIRzhcVE')

phone = None
lastname = None
firstname = None
middlename = None
userbirthday = None

usercitizenRF = None


geolocator = None
locationcity = None

cityname = 'Арзамас'



state = 'initial'  # Начальное состояние


@bot.message_handler(commands=['start'])
def registration(message):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, datatime current_timestamp, phone varchar(50), city varchar(50), last_name varchar(50), firts_name varchar(50), middle_name varchar(50), birthday data, citizenRF varchar(50))')
    conn.commit() 
    cur.close()
    conn.close()
    
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, '<b><em>Необходимо отправить контакт по кнопке внизу!</em></b>👇 \n\nПривет!\nДавай пройдём короткую регистрацию\n🤝\n\nДля начала - поделись номером телефона!\n👇👇👇👇👇', reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, geolocation)   

def geolocation(message):
    global phone
    try:
        phone = message.contact.phone_number
        global geolocator
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "⚠️Включи геолокацию на телефоне!⚠️\n\nОтправь свой город, чтобы получать заявки без ошибок👇👇👇\n\nℹ️Определение города может занять некоторое время🕰.", reply_markup=keyboard)
        bot.register_next_step_handler(message, location)
        geolocator = Nominatim(user_agent = "name_of_your_app")    
    except Exception:        
        bot.send_message(message.chat.id, '<b><em>Что-то пошло не так. Вам необходимо отправить контакт по КНОПКЕ внизу! \n\nЕсли вы её не видите, значит она скрыта и находится чуть правее от поля ввода сообщения</em></b>👇', parse_mode='html')
        bot.register_next_step_handler(message, geolocation)   


def city_state_country(coord):
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
    global geolocator
    global locationcity
    if message.location is not None:           
        a = [message.location.latitude, message.location.longitude]         
        city_name = city_state_country(a)
        locationcity = city_name
        bot.send_message(message.chat.id, f'✅Найден город {locationcity}', reply_markup=types.ReplyKeyboardRemove())

        found_city(message)   
        
    else:        
        bot.send_message(message.chat.id, '<b><em>Что-то пошло не так. Необходимо отправить геолокацию по КНОПКЕ внизу! \n\nЕсли вы её не видите, значит она скрыта и находится чуть правее от поля ввода сообщения</em></b>👇', parse_mode='html')
        bot.register_next_step_handler(message, location)   
        

def found_city(message):
    bot.send_message(message.chat.id, 'Еще пару шагов и мы у цели!\n🖌Введи <b>ТОЛЬКО</b> фамилию:', parse_mode='html')
    bot.register_next_step_handler(message, last_nameTrue)


# def last_name(message):
#     if len(message.text.strip()) > 50:
#         bot.send_message(message.chat.id, 'Слишком большое сообщение. Пожалуйста, введите корректную фамилию.')
#         found_city(message)         
#     else:
#         if len(message.text.strip()) <= 50:
#             last_nameTrue(message)
   

def last_nameTrue(message):
    global lastname
    if len(message.text.strip()) > 50:
        bot.send_message(message.chat.id, 'Слишком большое сообщение. Пожалуйста, введите корректную фамилию.')
        message.text.strip(None)
        found_city(message) 
    else:
        lastname = message.text.strip()
        print(lastname)
        testLastname(message)

def testLastname(message):
    bot.send_message(message.chat.id, '🖌Введи <b>ТОЛЬКО</b> имя:', parse_mode='html')
    bot.register_next_step_handler(message, first_name)

def first_name(message):       
    global firstname
    if len(message.text.strip()) > 50:
        bot.send_message(message.chat.id, 'Слишком большое сообщение. Пожалуйста, введите корректное имя.')
        message.text.strip(None)
        testLastname(message)        
    else:                  
        firstname = message.text.strip()    
        print(first_name)
        testFirstName(message)
        
def testFirstName(message):
    bot.send_message(message.chat.id, '🖌Введи <b>ТОЛЬКО</b> отчество:', parse_mode='html')
    bot.register_next_step_handler(message, middle_name)

# def first_nameTrue(message):
#     global firstname
#     firstname = message.text.strip()    
#     bot.send_message(message.chat.id, '🖌Введи <b>ТОЛЬКО</b> отчество:', parse_mode='html')
#     bot.register_next_step_handler(message, middle_name)

def middle_name(message):      
    global middlename
    if len(message.text.strip()) > 50:
        bot.send_message(message.chat.id, 'Слишком большое сообщение. Пожалуйста, введите корректное отчество.')
        message.text.strip(None)
        testFirstName(message) 
    else:     
        middlename = message.text.strip()
        print(middle_name)
        testMiddleName(message)

def testMiddleName(message):
    bot.send_message(message.chat.id, '🖌 Введи дату рождения в формате «день.месяц.год» пример: 01.01.1990', parse_mode='html')
    bot.register_next_step_handler(message, user_birthday)

# def middle_nameTrue(message):    
#     global middlename
#     middlename = message.text.strip()
#     bot.send_message(message.chat.id, '🖌 Введи дату рождения в формате «день.месяц.год» пример: 01.01.1990', parse_mode='html')
#     bot.register_next_step_handler(message, user_birthday)

def get_date(text):
    try:
        date = datetime.strptime(text, '%d.%m.%Y')
        return date.strftime('%d.%m.%Y')
    except ValueError:
        return None

def user_birthday(message):
    global userbirthday
    try:
        userbirthday = get_date(message.text.strip())
        if userbirthday:
            citizenRU(message)
        else:
            bot.send_message(message.chat.id, 'Не верный формат даты, необходимо ДД.ММ.ГГГГ')
            bot.register_next_step_handler(message, user_birthday)
    except ValueError:
        bot.send_message(message.chat.id, 'Не верный формат даты, необходимо ДД.ММ.ГГГГ')
        bot.register_next_step_handler(message, user_birthday)
# def user_birthday(message):
#     global userbirthday
#     try:
#         userbirthday = parse(message.text.strip())
#         citizenRU(message)
#     except ValueError:
#         bot.send_message(message.chat.id, 'Не верный формат даты, необходимо ДД-ММ-ГГГГ')
#         bot.register_next_step_handler(message, user_birthday)


def citizenRU(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Да', callback_data='delete', one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton('Нет', callback_data='edit', one_time_keyboard=True)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, 'Являешься гражданином Российской Федерации🇷🇺?', reply_markup=markup)  

@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
@bot.callback_query_handler(func=lambda callback: callback.data == 'edit') 
def callback_messageYes(callback):   
    global usercitizenRF 
    if callback.data == 'delete':
        usercitizenRF = 'Да'        
        bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', callback.message.chat.id, callback.message.message_id)

    else:          
        usercitizenRF = 'Нет'
        bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', callback.message.chat.id, callback.message.message_id)

    
    bot.send_message(callback.message.chat.id, f'📞 Телефон: +{phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: {usercitizenRF}\n🏙 Город(а): {locationcity}')
    user_pass(callback.message)

@bot.message_handler(content_types=['text'])
def get_photo(message):          
        global state
        if state == 'initial':         
            bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'<b>Не верный формат.</b> \n\nНажмите на кнопку соответствующую вашему гражданству', parse_mode='html')
            citizenRU(message)         
        elif state == 'citizenRU':
            # bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'<b>Регистрация прошла успешно!</b>', parse_mode='html')
            user_pass(message)
        else:
            bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', message.chat.id, message.message_id)



def user_pass(message):
    global usercitizenRF   
    global state  
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (phone, city, last_name, firts_name, middle_name, birthday, citizenRF) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF)) 
   
    conn.commit()
    cur.close()
    conn.close()
    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'👉Канал {cityname}', callback_data='users'))
       
    bot.send_message(message.chat.id, f'Готово🖖\nПереходи на канал «Арзамас» (там будут заявки)\n\nКак перейдёшь - обязательно нажми кнопку «начать/старт/start» (без этого заявки не будут появляться ‼️ )\n\n👇👇👇👇👇', reply_markup=markup)
    
    state = 'citizenRU'

# @bot.message_handler(content_types=['text'])
# def get_photo(message):       
#         bot.edit_message_text('Являешься гражданином Российской Федерации🇷🇺?', message.chat.id, message.message_id-1)
#         bot.send_message(message.chat.id, 'Не то')
#         user_pass(message)

@bot.callback_query_handler(func=lambda call: call.data == 'users')
def callback(call):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)
    print(info)



print('Bot started')

bot.polling(non_stop=True)