import telebot
from telebot import types
import sqlite3

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

adress = None
whattodo = None
timetostart = None
feedback = None
cityname = None
countPeople = None
salary = None
state = 'initial'


humanCount = None
needText = None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Сформировать заявку')
    btn2 = types.KeyboardButton('Открыть базу данных заявок')
    btn3 = types.KeyboardButton('Открыть базу данных пользователей')
    markup.row(btn1)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, 'Рад помочь, выберите подходящий пункт',  reply_markup=markup)
    bot.register_next_step_handler(message, city_of_obj)


def city_of_obj(message):
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        start(message) 
    else:
        if message.text == 'Сформировать заявку':
            bot.send_message(message.chat.id, "Напишите город объекта: ", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, city_of_obj_check)

        elif message.text == 'Открыть базу данных заявок':
            bot.send_message(message.chat.id, 'Вот база данных заявок: ')
            show_database_orders(message)
            start(message)
        elif message.text == 'Открыть базу данных пользователей':
            bot.send_message(message.chat.id, 'Вот база данных пользователей: ')
            show_database_users(message)
            start(message)
        else:
            bot.send_message(message.chat.id, 'Выберите подходящий пункт меню')            
            start(message)
  

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
            try:
                countPeople = message.text.strip()
                int(countPeople)
                input_lastname(message)
            except ValueError:
                bot.send_message(message.from_user.id, 'Введите цифру')
                registration(message)
            
        
def input_lastname(message):
    bot.send_message(message.chat.id, lastnameText, parse_mode='html')
    bot.register_next_step_handler(message, lastneme_check)   

def lastneme_check(message):
    global adress
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_lastname(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_lastname(message) 
        else:
            adress = message.text.strip()
            print(adress)
            input_firstname(message)

def input_firstname(message):
    bot.send_message(message.chat.id, firstnameText, parse_mode='html')
    bot.register_next_step_handler(message, firstname_check)

def firstname_check(message):       
    global whattodo
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_firstname(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_firstname(message)        
        else:                  
            whattodo = message.text.strip()    
            print(firstname_check)
            input_middlename(message)
        
def input_middlename(message):
    bot.send_message(message.chat.id, middlenameText, parse_mode='html')
    bot.register_next_step_handler(message, middlename_check)

def middlename_check(message):      
    global timetostart
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_middlename(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, middlenameError)
            message.text.strip(None)
            input_middlename(message) 
        else:     
            timetostart = message.text.strip()
            print(middlename_check)
            input_middlenam2(message)

def input_middlenam2(message):
    bot.send_message(message.chat.id, 'Напишите сумму в час:', parse_mode='html')
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
            try:
                salary = message.text.strip()                
                int(salary)
                print(middlename_check)
                citizenRU(message)
            except ValueError:
                bot.send_message(message.from_user.id, 'Введите число')
                input_middlenam2(message)
            
def citizenRU(message):
    global countPeople
    global humanCount
    global needText
    if (int(countPeople) <= 1) or (int(countPeople) >= 5):
        humanCount = 'человек'
    else:
        humanCount = 'человека'
    
    if int(countPeople) > 1:
        needText = 'Нужно'
    else:
        needText = 'Нужен'

    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b> {needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉{adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    start(message)

@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonYesTextCallbackData)
@bot.callback_query_handler(func=lambda callback: callback.data == citizenRuButtonNoTextCallbackData) 
def callback_message_citizen(callback):  
    global feedback 
    if callback.data == citizenRuButtonYesTextCallbackData:
        feedback = citizenRuButtonYesText        
        bot.edit_message_text(f'{userCitizenRuText}\n\n✅\n<b>·{cityname}: </b> {countPeople}\n<b>·Адрес:</b>👉{adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', callback.message.chat.id, callback.message.message_id, parse_mode='html')

    else:          
        feedback = citizenRuButtonNoText
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
    global state  
    conn = sqlite3.connect('./applicationbase.sql')
    cur = conn.cursor()
    cur.execute(insertIntoBase % (cityname, countPeople, adress, whattodo, timetostart, salary)) 

    conn.commit()
    cur.close()
    conn.close()    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {cityname}', url='https://t.me/ArJobBot'))
       
    bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    state = 'citizenRU'

def show_database_orders(message):
    conn = sqlite3.connect('./applicationbase.sql')
    cur = conn.cursor()
# SELECT * FROM users ORDER BY id DESC LIMIT для вывода последнего пользователя
    cur.execute('SELECT * FROM orders')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Заявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[7]}\n\n'
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)
    print(info)

def show_database_users(message):
    conn = sqlite3.connect('./peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Пользователь номер: {el[0]}, Дата регистрации: {el[1]}, Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n\n'

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)
    print(info)

print('Bot started')

bot.polling(non_stop=True)