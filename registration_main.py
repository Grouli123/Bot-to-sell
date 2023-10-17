import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime

import registration_people_config.registration_API_key as API_key
import registration_people_config.registration_sqlBase as sqlBase
import registration_people_config.registration_config_message as config_message

import citys.city_list as citys

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

samozanatost = 'Нет'
agreeaccaunt = 'Нет'
passport = 'Нет'

state = 'initial'

user_id = None

registered = False

arzCity = citys.arzamas
ekaCity = citys.ekaterenburg
sanCity = citys.sankt_peterburg

chatcity = None

cityTrue = 'False'

@bot.message_handler(commands=['start'])
def registration(message):
    global user_id
    
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    user_id = message.from_user.id
    cur.execute(base)
    conn.commit() 

    cur.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    existing_user = cur.fetchone()


    cur.close()
    conn.close()
    print(user_id)

    if existing_user is None:
        
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, phoneMessageText, reply_markup=keyboard, parse_mode='html')
        bot.register_next_step_handler(message, geolocation)   
    else:
        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()

        cur.execute("SELECT botchatname, city FROM users WHERE user_id = ('%s')" % (user_id))
        result = cur.fetchone()
        chatcity = result[0]
        locationcity = result[1]
        print(chatcity)


        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBase, url=f'https://t.me/{chatcity}'))
        
        bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)




def geolocation(message):    
    global phone
    try:
        phone = message.contact.phone_number
        if phone.startswith('+7') or phone.startswith('7'):
            global geolocator
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text=geolocationButtonText, request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id, geolocationMessageText, reply_markup=keyboard)
            bot.register_next_step_handler(message, location)
            geolocator = Nominatim(user_agent = geolocationNameApp)    
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, f"Недопустимый номер {phone}.\n\nПривет!\n\nДавай пройдём короткую регистрацию🤝Для начала - поделись номером телефона!👇👇👇👇👇", reply_markup=keyboard, parse_mode='html')
            bot.register_next_step_handler(message, geolocation)   
        
    except Exception:        
        bot.send_message(message.chat.id, phoneError, parse_mode='html')
        bot.register_next_step_handler(message, geolocation)   

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

        input_lastname(message)   
            
    else:        
        bot.send_message(message.chat.id, geolocationError, parse_mode='html')
        bot.register_next_step_handler(message, location)   
        
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
            input_birtgday(message)

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
    global userbirthday    
    try:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_birtgday(message)
        else:
            userbirthday = get_date(message.text.strip())
            if userbirthday:
                citizenRU(message)
            else:
                bot.send_message(message.chat.id, dateError)
                bot.register_next_step_handler(message, user_birthday_check)
    except ValueError:
        bot.send_message(message.chat.id, dateError)
        bot.register_next_step_handler(message, user_birthday_check)

def citizenRU(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)  

@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonYesTextCallbackData)
@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonNoTextCallbackData) 
def callback_message_citizen(callback):   
    global usercitizenRF 
    global registered
    if callback.data == citizenRuButtonYesTextCallbackData:
        usercitizenRF = citizenRuButtonYesText        
        bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    else:          
        usercitizenRF = citizenRuButtonNoText
        bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    registered = True
    bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: {usercitizenRF}\n🏙 Город(а): {locationcity}')
    city_check_for_chat(callback.message)

@bot.message_handler(content_types=['text'])
def check_callback_message_citizen(message):          
        global state      
        if state == 'initial':         
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            citizenRU(message)         
        elif state == 'citizenRU':
            bot.send_message(message.chat.id, registrationSucsess, parse_mode='html')
            city_check_for_chat(message)
        else:
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id)

def city_check_for_chat(message):
    global chatcity
    if locationcity == 'Арзамас':
        chatcity = arzCity        
        import_into_database(message)
    elif locationcity == 'Екатеринбург':
        chatcity = ekaCity
        import_into_database(message)
    elif locationcity == 'Санкт-Петербург':
        chatcity = sanCity
        import_into_database(message)
    else:
        bot.send_message(message.chat.id, 'К сожалению, мы не работаем по вашему городу')

def import_into_database(message):
    global usercitizenRF   
    global state  
    global cityTrue
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    cur.execute(insertIntoBase % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF, user_id, samozanatost, agreeaccaunt, passport, chatcity, cityTrue)) 
   
    conn.commit()
    cur.close()
    conn.close()
    
    print (cityTrue)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBase, url=f'https://t.me/{chatcity}'))
       
    bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    state = 'citizenRU'

print('Bot started')

bot.polling(non_stop=True)