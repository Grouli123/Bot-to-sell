import telebot
from telebot import types
import sqlite3

import admin_config.admin_API_key as API_key_one
import admin_config.admin_sqlBase as sqlBase_one
import admin_config.admin_config_message as config_message_one

import get_orders_config.get_orders_API_key as API_key_Test



import get_orders_config.get_orders_config_message as config_message_bot_order

botApiKey = API_key_one.botAPI
botApiKeyTwo = API_key_Test.botAPI

bot1 = telebot.TeleBot(botApiKey)
bot2 = telebot.TeleBot(botApiKeyTwo)

base1 = sqlBase_one.createDatabase
insertIntoBase1 = sqlBase_one.insertIntoDatabase
nameOfBase1 = sqlBase_one.name_of_base

maxSymbol1 = config_message_one.max_symbol_for_message

adressText = config_message_one.input_adress_text
adressError = config_message_one.adress_error

whatToDoText = config_message_one.input_whattodo_text
whatToDoError = config_message_one.whattodo_error

startWorkText = config_message_one.input_startwork_text
startWorkError = config_message_one.startwork_error

textOnly = config_message_one.message_should_be_text_type

orderSendText = config_message_one.order_send
orderSendTextCallbackData = config_message_one.order_send_callback_data

orderDeleteText = config_message_one.order_delete
orderDeleteCallbackData = config_message_one.order_delete_callback_data

userCitizenRuText = config_message_one.ready_order_text
userCitizenRuError = config_message_one.ready_order_error

orderSucsess = config_message_one.order_sucsess
buttonResultName = config_message_one.button_result_name

alreadyRegistered = config_message_one.already_registered

makeOrderButton = config_message_one.make_order_button
openBaseOrders = config_message_one.open_base_orders
openBasePeople = config_message_one.open_base_people
startBotMessage = config_message_one.start_bot_message

inputCityObject = config_message_one.input_city_object

openBseOrdersMessage = config_message_one.open_base_orders_message
openBasePeopleMessage = config_message_one.open_base_people_message
chooseTruePointOfMenu = config_message_one.choose_true_point_of_menu

inputCountOfNeedPeople = config_message_one.input_count_of_need_people
inputNumber = config_message_one.input_number

inputSumInHour = config_message_one.input_sum_in_hour

inputNumbers = config_message_one.input_numbers



citizenRuButtonYesTextOne = config_message_bot_order.citizen_ru_button_yes
citizenRuButtonYesTextCallbackDataOne = config_message_bot_order.citizen_ru_button_yes_callback_data

citizenRuButtonNoTextOne = config_message_bot_order.citizen_ru_button_no
citizenRuButtonNoTextCallbackDataOne = config_message_bot_order.citizen_ru_button_no_callback_data




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







@bot1.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton(makeOrderButton)
    btn2 = types.KeyboardButton(openBaseOrders)
    btn3 = types.KeyboardButton(openBasePeople)
    markup.row(btn1)
    markup.row(btn2, btn3)    
    bot1.send_message(message.chat.id, startBotMessage,  reply_markup=markup)
    bot1.register_next_step_handler(message, city_of_obj)

def city_of_obj(message):
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        start(message) 
    else:
        if message.text == makeOrderButton:
            bot1.send_message(message.chat.id, inputCityObject, reply_markup=types.ReplyKeyboardRemove())
            bot1.register_next_step_handler(message, city_of_obj_check)

        elif message.text == openBaseOrders:
            bot1.send_message(message.chat.id, openBseOrdersMessage)
            show_database_orders(message)
            start(message)
        elif message.text == openBasePeople:
            bot1.send_message(message.chat.id, openBasePeopleMessage)
            show_database_users(message)
            start(message)
        else:
            bot1.send_message(message.chat.id, chooseTruePointOfMenu)            
            start(message)  

def city_of_obj_check(message):
    global cityname
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        city_of_obj(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            message.text.strip(None)
            city_of_obj(message) 
        else:
            cityname = message.text.strip()
            print(cityname)            
            people_need_count(message)

def people_need_count(message):
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()

    cur.execute(base1)
    conn.commit() 
    cur.close()
    conn.close()
    bot1.send_message(message.chat.id, inputCountOfNeedPeople, parse_mode='html')
    bot1.register_next_step_handler(message, people_need_count_check)   

def people_need_count_check(message):
    global countPeople
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        people_need_count(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            message.text.strip(None)
            people_need_count(message) 
        else:
            try:
                countPeople = message.text.strip()
                int(countPeople)
                input_adress(message)
            except ValueError:
                bot1.send_message(message.from_user.id, inputNumber)
                people_need_count(message)
            
        
def input_adress(message):
    bot1.send_message(message.chat.id, adressText, parse_mode='html')
    bot1.register_next_step_handler(message, adress_check)   

def adress_check(message):
    global adress
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_adress(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_adress(message) 
        else:
            adress = message.text.strip()
            print(adress)
            input_whattodo(message)

def input_whattodo(message):
    bot1.send_message(message.chat.id, whatToDoText, parse_mode='html')
    bot1.register_next_step_handler(message, whattodo_check)

def whattodo_check(message):       
    global whattodo
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_whattodo(message)
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, whatToDoError)
            message.text.strip(None)
            input_whattodo(message)        
        else:                  
            whattodo = message.text.strip()    
            print(whattodo_check)
            input_startwork(message)
        
def input_startwork(message):
    bot1.send_message(message.chat.id, startWorkText, parse_mode='html')
    bot1.register_next_step_handler(message, startwork_check)

def startwork_check(message):      
    global timetostart
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_startwork(message)
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, startWorkError)
            message.text.strip(None)
            input_startwork(message) 
        else:     
            timetostart = message.text.strip()
            print(startwork_check)
            input_salary(message)

def input_salary(message):
    bot1.send_message(message.chat.id, inputSumInHour, parse_mode='html')
    bot1.register_next_step_handler(message, salary_check)

def salary_check(message):      
    global salary
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_salary(message)
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, startWorkError)
            message.text.strip(None)
            input_salary(message) 
        else:     
            try:
                salary = message.text.strip()                
                int(salary)
                print(startwork_check)
                created_order(message)
            except ValueError:
                bot1.send_message(message.from_user.id, inputNumbers)
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
    bot1.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    # start(message)

@bot1.callback_query_handler(func=lambda callback: callback.data == orderSendTextCallbackData)
@bot1.callback_query_handler(func=lambda callback: callback.data == orderDeleteCallbackData) 
def callback_message_created_order(callback):  
    global feedback 
    global my_variable
    if callback.data == orderSendTextCallbackData:

        conn = sqlite3.connect('user_data.sql')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users")
        user_ids = cursor.fetchall()

        
        feedback = orderSendText     
        bot1.send_message(callback.message.chat.id, userCitizenRuText,parse_mode='html')
        application = f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html')
        
        for user_id_test in user_ids:

            try:
                # bot2.send_message(user_id[0], "Привет от первого бота!")
                markup2 = types.InlineKeyboardMarkup()
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data=citizenRuButtonYesTextCallbackDataOne, one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data=citizenRuButtonNoTextCallbackDataOne, one_time_keyboard=True)
                btn32 = types.InlineKeyboardButton('Едем в 3', callback_data=citizenRuButtonNoTextCallbackDataOne, one_time_keyboard=True)
                btn42 = types.InlineKeyboardButton('Едем в 4', callback_data=citizenRuButtonNoTextCallbackDataOne, one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', callback_data=citizenRuButtonNoTextCallbackDataOne, one_time_keyboard=True)
                markup2.row(btn12)  
                markup2.row(btn22)  
                markup2.row(btn32)  
                markup2.row(btn42)  
                markup2.row(btn52) 
                bot2.send_message(user_id_test[0], f'{application}', reply_markup=markup2, parse_mode='html') # Замените 'CHAT_ID_BOT2' на ID чата второго бота

            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id_test[0]}: {str(e)}")

        conn.close()
    else:          
        feedback = orderDeleteText
        bot1.delete_message(callback.message.chat.id, callback.message.message_id)
    
    import_into_database(callback.message)

@bot1.message_handler(content_types=['text'])
def check_callback_message_ready_order(message):          
        global state      
        if state == 'initial':         
            bot1.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot1.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            created_order(message)         
        elif state == 'citizenRU':
            bot1.send_message(message.chat.id, orderSucsess, parse_mode='html')
            import_into_database(message)
        else:
            bot1.edit_message_text(userCitizenRuText, message.chat.id, message.message_id)

def import_into_database(message):
    global state  
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()
    cur.execute(insertIntoBase1 % (cityname, countPeople, adress, whattodo, timetostart, salary)) 

    conn.commit()
    cur.close()
    conn.close()    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {cityname}', url='https://t.me/ArJobBot'))
       
    bot1.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    state = 'citizenRU'
    start(message)

def show_database_orders(message):
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()
# SELECT * FROM users ORDER BY id DESC LIMIT для вывода последнего пользователя
    cur.execute('SELECT * FROM orders')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Заявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[7]}\n\n'
    cur.close()
    conn.close()

    bot1.send_message(message.chat.id, info)
    print(info)

def show_database_users(message):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Пользователь номер: {el[0]}, Дата регистрации: {el[1]}, Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}\n\n'

    cur.close()
    conn.close()

    bot1.send_message(message.chat.id, info)
    print(info)

print('Bot started')

bot1.polling(non_stop=True)