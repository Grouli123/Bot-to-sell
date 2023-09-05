import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from geopy.geocoders import Nominatim
import time


bot = telebot.TeleBot('6484701618:AAFcxH0T31Rl_XakKMfFm5PWsLwSIRzhcVE')

phone = None
lastname = None
firstname = None
middlename = None
userbirthday = None

citizenRF = None

dataYesOrNo = None

geolocator = None
locationcity = None

cityname = 'Арзамас'

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
    phone = message.contact.phone_number
    global geolocator
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "⚠️Включи геолокацию на телефоне!⚠️\n\nОтправь свой город, чтобы получать заявки без ошибок👇👇👇\n\nℹ️Определение города может занять некоторое время🕰.", reply_markup=keyboard)
    bot.register_next_step_handler(message, location)
    geolocator = Nominatim(user_agent = "name_of_your_app")    

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
        found_city(message)
        print('вот ',message)

def found_city(message):
    bot.send_message(message.chat.id, f'✅Найден город {locationcity}')
    bot.send_message(message.chat.id, 'Еще пару шагов и мы у цели!\n🖌Введи <b>ТОЛЬКО</b> фамилию:', parse_mode='html')
    bot.register_next_step_handler(message, last_name)

def last_name(message):
    global lastname
    print('fuf')
    lastname = message.text.strip()
    bot.send_message(message.chat.id, '🖌Введи <b>ТОЛЬКО</b> имя:', parse_mode='html')
    bot.register_next_step_handler(message, first_name)
    print(lastname)

def first_name(message):
    global firstname
    firstname = message.text.strip()    
    bot.send_message(message.chat.id, '🖌Введи <b>ТОЛЬКО</b> отчество:', parse_mode='html')

    bot.register_next_step_handler(message, middle_name)
    print(firstname)

def middle_name(message):
    global middlename
    middlename = message.text.strip()
    bot.send_message(message.chat.id, '🖌 Введи дату рождения в формате «день.месяц.год» пример: 01.01.1990', parse_mode='html')
    bot.register_next_step_handler(message, user_birthday)
    print(middlename, firstname, lastname)

def user_birthday(message):
    global userbirthday
    userbirthday = message.text.strip()
    get_photo(message)






def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Да', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Нет', callback_data='edit')
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, 'Являешься гражданином Российской Федерации🇷🇺?', reply_markup=markup)
    


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):   
    global dataYesOrNo
    global citizenRF 
    if callback.data == 'delete':
        bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: Есть\n🏙 Город(а): {locationcity}')
        dataYesOrNo = 'Да'
        user_pass(callback.message)

    elif callback.data == 'edit':
        bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: Нет\n🏙 Город(а): {locationcity}')
        dataYesOrNo = 'Нет'
        user_pass(callback.message)
    citizenRF = dataYesOrNo
    print(citizenRF)
    

# def check_status(message):
#     global citizenRF
#     if citizenRF is not None:
#         bot.register_next_step_handler(message, user_pass)

#         print(citizenRF)

#     else:
#         print('Ошибка')




def user_pass(message):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (phone, city, last_name, firts_name, middle_name, birthday, citizenRF) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (phone, locationcity, lastname, firstname, middlename, userbirthday, citizenRF)) 
   
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'👉Канал {cityname}', callback_data='users'))
    bot.send_message(message.chat.id, f'Готово🖖\nПереходи на канал «Арзамас» (там будут заявки)\n\nКак перейдёшь - обязательно нажми кнопку «начать/старт/start» (без этого заявки не будут появляться ‼️ )\n\n👇👇👇👇👇', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Номер телефона: {el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)
    print(info)

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)

print('Bot started')

bot.polling(non_stop=True)