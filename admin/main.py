import telebot
from telebot import types
import sqlite3

import config.API_key
import sqlBase as sqlBase
import config_message

botApiKey = config.API_key.botAPI

bot = telebot.TeleBot(botApiKey)

base = sqlBase.createDatabase
insertIntoBase = sqlBase.insertIntoDatabase
nameOfBase = sqlBase.name_of_base

maxSymbol = config_message.max_symbol_for_message

adressText = config_message.input_adress_text
adressError = config_message.adress_error

whatToDoText = config_message.input_whattodo_text
whatToDoError = config_message.whattodo_error

startWorkText = config_message.input_startwork_text
startWorkError = config_message.startwork_error

textOnly = config_message.message_should_be_text_type

orderSendText = config_message.order_send
orderSendTextCallbackData = config_message.order_send_callback_data

orderDeleteText = config_message.order_delete
orderDeleteCallbackData = config_message.order_delete_callback_data

userCitizenRuText = config_message.ready_order_text
userCitizenRuError = config_message.ready_order_error

orderSucsess = config_message.order_sucsess
buttonResultName = config_message.button_result_name

alreadyRegistered = config_message.already_registered

makeOrderButton = config_message.make_order_button
openBaseOrders = config_message.open_base_orders
openBasePeople = config_message.open_base_people
startBotMessage = config_message.start_bot_message

inputCityObject = config_message.input_city_object

openBseOrdersMessage = config_message.open_base_orders_message
openBasePeopleMessage = config_message.open_base_people_message
chooseTruePointOfMenu = config_message.choose_true_point_of_menu

inputCountOfNeedPeople = config_message.input_count_of_need_people
inputNumber = config_message.input_number

inputSumInHour = config_message.input_sum_in_hour

inputNumbers = config_message.input_numbers

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
    btn1 = types.KeyboardButton(makeOrderButton)
    btn2 = types.KeyboardButton(openBaseOrders)
    btn3 = types.KeyboardButton(openBasePeople)
    markup.row(btn1)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, startBotMessage,  reply_markup=markup)
    bot.register_next_step_handler(message, city_of_obj)


def city_of_obj(message):
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        start(message) 
    else:
        if message.text == makeOrderButton:
            bot.send_message(message.chat.id, inputCityObject, reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, city_of_obj_check)

        elif message.text == openBaseOrders:
            bot.send_message(message.chat.id, openBseOrdersMessage)
            show_database_orders(message)
            start(message)
        elif message.text == openBasePeople:
            bot.send_message(message.chat.id, openBasePeopleMessage)
            show_database_users(message)
            start(message)
        else:
            bot.send_message(message.chat.id, chooseTruePointOfMenu)            
            start(message)
  

def city_of_obj_check(message):
    global cityname
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        city_of_obj(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, adressError)
            message.text.strip(None)
            city_of_obj(message) 
        else:
            cityname = message.text.strip()
            print(cityname)            
            people_need_count(message)

def people_need_count(message):
    conn = sqlite3.connect('./applicationbase.sql')
    cur = conn.cursor()

    cur.execute(base)
    conn.commit() 
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, inputCountOfNeedPeople, parse_mode='html')
    bot.register_next_step_handler(message, people_need_count_check)   

def people_need_count_check(message):
    global countPeople
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        people_need_count(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, adressError)
            message.text.strip(None)
            people_need_count(message) 
        else:
            try:
                countPeople = message.text.strip()
                int(countPeople)
                input_adress(message)
            except ValueError:
                bot.send_message(message.from_user.id, inputNumber)
                people_need_count(message)
            
        
def input_adress(message):
    bot.send_message(message.chat.id, adressText, parse_mode='html')
    bot.register_next_step_handler(message, adress_check)   

def adress_check(message):
    global adress
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_adress(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_adress(message) 
        else:
            adress = message.text.strip()
            print(adress)
            input_whattodo(message)

def input_whattodo(message):
    bot.send_message(message.chat.id, whatToDoText, parse_mode='html')
    bot.register_next_step_handler(message, whattodo_check)

def whattodo_check(message):       
    global whattodo
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_whattodo(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, whatToDoError)
            message.text.strip(None)
            input_whattodo(message)        
        else:                  
            whattodo = message.text.strip()    
            print(whattodo_check)
            input_startwork(message)
        
def input_startwork(message):
    bot.send_message(message.chat.id, startWorkText, parse_mode='html')
    bot.register_next_step_handler(message, startwork_check)

def startwork_check(message):      
    global timetostart
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_startwork(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, startWorkError)
            message.text.strip(None)
            input_startwork(message) 
        else:     
            timetostart = message.text.strip()
            print(startwork_check)
            input_salary(message)

def input_salary(message):
    bot.send_message(message.chat.id, inputSumInHour, parse_mode='html')
    bot.register_next_step_handler(message, salary_check)

def salary_check(message):      
    global salary
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_salary(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, startWorkError)
            message.text.strip(None)
            input_salary(message) 
        else:     
            try:
                salary = message.text.strip()                
                int(salary)
                print(startwork_check)
                created_order(message)
            except ValueError:
                bot.send_message(message.from_user.id, inputNumbers)
                input_salary(message)
            
def created_order(message):
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
    btn2 = types.InlineKeyboardButton(orderSendText, callback_data=orderSendTextCallbackData, one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton(orderDeleteText, callback_data=orderDeleteCallbackData, one_time_keyboard=True)
    markup.row(btn2, btn3)    
    bot.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    # start(message)

@bot.callback_query_handler(func=lambda callback: callback.data == orderSendTextCallbackData)
@bot.callback_query_handler(func=lambda callback: callback.data == orderDeleteCallbackData) 
def callback_message_created_order(callback):  
    global feedback 
    if callback.data == orderSendTextCallbackData:
        feedback = orderSendText        
        bot.edit_message_text(f'{userCitizenRuText}\n\n✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', callback.message.chat.id, callback.message.message_id, parse_mode='html')

    else:          
        feedback = orderDeleteText
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    import_into_database(callback.message)

@bot.message_handler(content_types=['text'])
def check_callback_message_ready_order(message):          
        global state      
        if state == 'initial':         
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            created_order(message)         
        elif state == 'citizenRU':
            bot.send_message(message.chat.id, orderSucsess, parse_mode='html')
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
    start(message)

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