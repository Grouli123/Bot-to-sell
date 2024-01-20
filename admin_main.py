import telebot
from telebot import types
import sqlite3
import json

import admin_config.admin_API_key as API_key_one
import admin_config.admin_sqlBase as sqlBase_one
import admin_config.admin_config_message as config_message_one

import get_orders_config.get_orders_API_key as API_key_Test



import get_orders_config.get_orders_config_message as config_message_bot_order


import citys.city_list as citys

# admin_main.py
# from observable import Observable

# admin_bot = Observable()



from get_orders_main import testMethod

botApiKey = API_key_one.botAPI

arzamasBot = API_key_Test.botAPIArz
# ekaterinburgBot = API_key_Test.botAPIEka
# sankt_peterburgBot = API_key_Test.botAPISan


bot_to_send = None

bot1 = telebot.TeleBot(botApiKey)
bot2 = telebot.TeleBot(arzamasBot)
# bot3 = telebot.TeleBot(ekaterinburgBot)
# bot4 = telebot.TeleBot(sankt_peterburgBot)

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
orderTime = None
feedback = None
cityname = None
countPeople = None
salary = None
state = 'initial'

humanCount = None
needText = None


arzCity = citys.arzamas
ekaCity = citys.ekaterenburg
sanCity = citys.sankt_peterburg
mosCity = citys.moskow

chatcity = None


login = 'admin'
password = 'admin123'

loginin = False

adminChatId = None
sent_message_id = None

user_message_ids = {}

user_id_two = None


users_who_clicked = []

user_name = None

take_user_id_id = None


test123 = None

def start(message):    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton(makeOrderButton)
    btn2 = types.KeyboardButton(openBaseOrders)
    btn3 = types.KeyboardButton(openBasePeople)
    markup.row(btn1)
    markup.row(btn2, btn3)    
    bot1.send_message(message.chat.id, startBotMessage,  reply_markup=markup)
    bot1.register_next_step_handler(message, city_of_obj)

@bot1.message_handler(commands=['start'])
def input_admin(message):      
    global adminChatId
    adminChatId = message.chat.id  # Получаем chat_id из сообщения

    print(loginin)

    if loginin == False:
        bot1.send_message(message.chat.id, 'Введите логин', parse_mode='html')
        bot1.register_next_step_handler(message, admin_check)   
    else:
        start(message)


def admin_check(message):
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_admin(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_admin(message) 
        else:
            if login == message.text.strip():
                input_password(message)
            else:
                bot1.send_message(message.from_user.id, 'Логин не найден')
                input_admin(message)

def input_password(message):
    bot1.send_message(message.chat.id, 'Введите пароль', parse_mode='html')
    bot1.register_next_step_handler(message, password_check)   

def password_check(message):
    global loginin
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_password(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_password(message) 
        else:
            if password == message.text.strip():
                loginin = True
                start(message)
            else:
                bot1.send_message(message.from_user.id, 'Пароль не подходит')
                input_password(message)


# def city_check_for_chat(message):
#     global chatcity
    
#     global arzamasBot 
#     global ekaterinburgBot
#     global sankt_peterburgBot
    
#     global bot_to_send

#     if cityname == 'Арзамас':
#         chatcity = arzCity    
#         bot_to_send = arzamasBot
#         import_into_database(message)
#     elif cityname == 'Екатеринбург':
#         chatcity = ekaCity
#         bot_to_send = ekaterinburgBot
#         import_into_database(message)
#     elif cityname == 'Санкт-Петербург':
#         chatcity = sanCity
#         bot_to_send = sankt_peterburgBot
#         import_into_database(message)
#     else:
#         bot1.send_message(message.chat.id, 'К сожалению, мы не работаем по вашему городу')
#         city_of_obj(message)


def city_of_obj(message):
    if loginin == True:
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
    else:
        bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)


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
    global sent_message_id
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
    sent_message = bot1.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> в {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    # start(message)
    sent_message_id = sent_message.message_id


# def get_value(testTest):
#     testTest = False
#     return testTest


@bot1.callback_query_handler(func=lambda callback: callback.data == orderSendTextCallbackData)
@bot1.callback_query_handler(func=lambda callback: callback.data == orderDeleteCallbackData) 
def callback_message_created_order(callback):  
    global feedback 
    global chatcity
    
    if callback.data == orderSendTextCallbackData:
        feedback = orderSendText     

        application = f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> в {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        
        markup1 = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup1.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, reply_markup=markup1, parse_mode='html')

        print(sent_message_id)
        if cityname == 'Арзамас':
            chatcity = arzCity
        elif cityname == 'Екатеринбург':                    
            chatcity = ekaCity
        elif cityname == 'Санкт-Петербург':                    
            chatcity = sanCity           
        elif cityname == 'Москва':
            chatcity = mosCity

        # admin_main.py
        # admin_bot.value = "Ваше сообщение здесь"
    else:          
        feedback = orderDeleteText
        bot1.delete_message(callback.message.chat.id, callback.message.message_id)
    
    import_into_database(callback.message)



@bot1.callback_query_handler(func=lambda callback: callback.data == '❌ Закрыть заявку')
def callback_message_created_order(callback):  
    if callback.data == '❌ Закрыть заявку':
        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        # sent_message = bot.send_message(message.chat.id, order_info, reply_markup=markup2, parse_mode='html')
        # last_message_id = sent_message.message_id  
        
        # users = cursor.fetchone()
        
        message_id = callback.message.message_id
        sql_query = "UPDATE orders SET actualMess = ('%s') WHERE adminMessageId = ('%s')"
        cursor.execute(sql_query % ('False' , message_id))

        cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary FROM orders WHERE adminMessageId = ('%s')" % (message_id))
        test2 = cursor.fetchone()
                    # Коммит изменений в базу данных
        conn.commit()

                    # Закрытие соединения с базой данных
        conn.close()
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
        markup.row(btn02)

        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
        print("все произошло")


        # # Находим идентификатор последней строки
        # cursor.execute('SELECT MAX(id) FROM orders')
        # max_id = cursor.fetchone()[0]

        # # Удаляем строку с максимальным идентификатором (последнюю строку)
        # if max_id is not None:
        #     cursor.execute("DELETE FROM orders WHERE id = ('%s')" % (max_id))
        #     conn.commit()
        #     print(f"Удалена строка с идентификатором {max_id}")
        # else:
        #     print("База данных пуста или произошла ошибка.")
        # conn.close()
        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()
        
        # cur.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 1')
        cur.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, orderMessageId, orderChatId FROM orders WHERE adminMessageId = ('%s')" % (message_id))

        users = cur.fetchone() 
        order_info_close = f'❌ Заявка закрыта\n<b>•{users[0]}: </b>{needText} {users[1]} {humanCount}\n<b>•Адрес:</b>👉 {users[2]}\n<b>•Что делать:</b> {users[3]}\n<b>•Начало работ:</b> в {users[4]}\n<b>•Вам на руки:</b> <u>{users[5]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        user_message_ids = users[6]
        chat_id_list = users[7].split(',') if users[7] else []
        message_id_list = user_message_ids.split(',') if user_message_ids else []
        conn.close()
        for chat_id, message_id in zip(chat_id_list, message_id_list):
            print('Чат id: ',chat_id)
            print('Месседж id: ', message_id)

            bot2.edit_message_text(order_info_close, chat_id, message_id, parse_mode='html')

        # order_message_id_str = cursor.fetchone()[0]

        # message_id_list = user_message_ids.split(',') if user_message_ids else []
        # chat_id_list = test.split (',') if test else []
        # # Закрытие соединения с базой данных
        # for user_id_mess in user_message_ids.keys():
        #     cursor.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % user_id_mess)
        #     order_message_id_str = cursor.fetchone()[0]
        #     print('Работает')
            # Разбейте строку orderMessageId на список message_id
            # message_id_list = order_message_id_str.split(',') if order_message_id_str else []

            # Измените сообщение для каждого message_id
        # for chat_id in chat_id_list:

        #     for message_id in message_id_list:
        #         print('работает2')
        #         print(message_id)

        #         bot2.edit_message_text(order_info_close, chat_id, message_id, parse_mode='html')
                                                    # нужно поменять callback.message.chat.id на чат id который будет меняться
                    # Закрытие соединения с базой данных
    

# def update_message_with_users_list(chat_id, message_id, test, user_id, users_who_clicked):
#     global user_id_two
#     user_id_two = user_id
#     print('в админке юзер айди это ', user_id_two)
#     conn3 = sqlite3.connect('applicationbase.sql')
#     cur3 = conn3.cursor()
#     cur3.execute("SELECT orderMessageId, adminChatId, adminMessageId FROM orders")
#     rows = cur3.fetchall() 
#     for row in rows:
#         order_message_ids = row[0].split(',')
#         admin_chat_id = row[1]
#         admin_message_id = row[2]


#     if str(test) in order_message_ids:
#             markup = types.InlineKeyboardMarkup()
#             for user_id in users_who_clicked:
#                 user_name = get_user_name_from_database(user_id)
#                 btn = types.InlineKeyboardButton(str(user_name), callback_data=f'user_{user_id}')
#                 print(print(f"Значение user_{user_id}"))
#                 markup.row(btn)
#             bot1.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_message_id, reply_markup=markup)
    

# def get_user_name_from_database(user_id):
#     conn = sqlite3.connect('peoplebase.sql')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
#     takeParam2 = cursor.fetchone()
#     if takeParam2:
#         user_lastname = takeParam2[4]
#         user_firstname = takeParam2[5] 
#         user_middlename = takeParam2[6]
#         user_name = user_lastname + ' ' + user_firstname + ' ' + user_middlename# Предположим, что имя пользователя находится во второй колонке
#         print('тут это', user_name)
#         return user_name

# def set_user_id():
#     global user_id_two
#     user_id_two = get_user_id()
#     return user_id_two


# def update_message_with_users_list(chat_id, message_id, test, user_id, users_who_clicked):
#     conn3 = sqlite3.connect('applicationbase.sql')
#     cur3 = conn3.cursor()
#     cur3.execute("SELECT orderMessageId, adminChatId, adminMessageId, whoTakeId FROM orders")
#     rows = cur3.fetchall() 
#     for row in rows:
#         order_message_ids = row[0].split(',')
#         admin_chat_id = row[1]
#         admin_message_id = row[2]        
#         how_take = row[3]


#     if str(test) in order_message_ids:
#             markup = types.InlineKeyboardMarkup()
#             for user_id in users_who_clicked:
#                 user_name = get_user_name_from_database(user_id)
#                 btn = types.InlineKeyboardButton(str(user_name), callback_data=f'user_')
#                 print(print(f"Значение user_{user_id}"))
#                 markup.row(btn)
#             bot1.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_message_id, reply_markup=markup)
    

# def get_user_name_from_database(user_id):
#     conn = sqlite3.connect('peoplebase.sql')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
#     takeParam2 = cursor.fetchone()
#     if takeParam2:
#         user_lastname = takeParam2[4]
#         user_firstname = takeParam2[5] 
#         user_middlename = takeParam2[6]
#         user_name = user_lastname + ' ' + user_firstname + ' ' + user_middlename# Предположим, что имя пользователя находится во второй колонке
#         print('тут это', user_name)
#         return user_name
    

def update_message_with_users_list_test(test):
    global take_user_id
    conn3 = sqlite3.connect('applicationbase.sql')
    cur3 = conn3.cursor()
    cur3.execute("SELECT adminChatId, adminMessageId, whoTakeId FROM orders")
    rows = cur3.fetchall()

    for row in rows:
        admin_chat_id = row[0]
        admin_message_id = row[1]
        who_take_ids = row[2].split(',') if row[2] else []  # Разбиваем whoTakeId на отдельные идентификаторы

        if str(test) in admin_message_id:
            markup = types.InlineKeyboardMarkup()
            for take_user_id in who_take_ids:
                user_name = get_user_name_from_database(take_user_id)
                if user_name is not None:
                    btn = types.InlineKeyboardButton(str(user_name), callback_data=f'user_{take_user_id}')
                    markup.row(btn)
                    
            btn02 = types.InlineKeyboardButton('Свернуть', callback_data='Свернуть1', one_time_keyboard=True)


            markup.row(btn02)
            bot1.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_message_id, reply_markup=markup)
       



def update_message_with_users_list(test):
    conn3 = sqlite3.connect('applicationbase.sql')
    cur3 = conn3.cursor()
    cur3.execute("SELECT adminChatId, adminMessageId, whoTakeId FROM orders")
    rows = cur3.fetchall()
    
    for row in rows:
        admin_chat_id = row[0]
        admin_message_id = row[1]
        who_take_ids = row[2].split(',') if row[2] else []

        if str(test) in admin_message_id:
            markup = types.InlineKeyboardMarkup()
            for take_user_id in who_take_ids:
                user_name = get_user_name_from_database(take_user_id)
                if user_name is not None:
                    btn = types.InlineKeyboardButton(str(user_name), callback_data=f'user_{take_user_id}')
                    markup.row(btn)

            btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
            btn02 = types.InlineKeyboardButton('Свернуть', callback_data='Свернуть', one_time_keyboard=True)

            markup.row(btn01)
            markup.row(btn02)
            bot1.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_message_id, reply_markup=markup)



def get_user_name_from_database(user_id):
    global user_name
    print('юзер айди в админке', user_id, type(user_id))
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ('%s')" % (user_id))
    takeParam2 = cursor.fetchone()
    if takeParam2:
        user_lastname = takeParam2[4]
        user_firstname = takeParam2[5]
        user_middlename = takeParam2[6]
        user_name = f"{user_lastname} {user_firstname} {user_middlename}"
        return user_name
    else:
        print('база данных: ', user_name)
        # return None





@bot1.callback_query_handler(func=lambda callback: callback.data == 'Свернуть1')
def testmess_close_one(callback):
    markup = types.InlineKeyboardMarkup()
    btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
    markup.row(btn02)
    bot1.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)
    


@bot1.callback_query_handler(func=lambda callback: callback.data == 'Свернуть')
def testmess_close(callback):
    markup = types.InlineKeyboardMarkup()
    btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
    btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину', one_time_keyboard=True)
    markup.row(btn02)
    markup.row(btn01)
    bot1.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

    
@bot1.callback_query_handler(func=lambda callback: callback.data == 'ОтправленоАдмину1')
def testmess_sendAdOne(callback):
    test = callback.message.message_id
    update_message_with_users_list_test(test)


@bot1.callback_query_handler(func=lambda callback: callback.data == 'ОтправленоАдмину')
def testmess_sendAd(callback):
    test = callback.message.message_id
    update_message_with_users_list(test)

 
@bot1.callback_query_handler(func=lambda callback: callback.data.startswith('user_'))
def testmess(callback):
    take_user_id = callback.data.split('_')[1]
    print('Идентификатор пользователя:', take_user_id)

    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ('%s')" % (take_user_id))
    takeParam2 = cursor.fetchone()
    

    if takeParam2:
        user_lastname = takeParam2[4]
        user_firstname = takeParam2[5]
        user_middlename = takeParam2[6]
        user_name = user_lastname + ' ' + user_firstname + ' ' + user_middlename
        print('тут это', user_name)
        print('в админке работает все ', user_name)

        cursor.close()
        conn.close()
        application = f'📞 Телефон: +{takeParam2[2]}\n👤 ФИО: {takeParam2[4]} {takeParam2[5]} {takeParam2[6]}\n📅 Дата рождения: {takeParam2[7]}\n🇷🇺 Гражданство РФ: {takeParam2[8]}\n🤝 Самозанятый: {takeParam2[10]} \n🏙 Город(а): {takeParam2[3]}'

        markup = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='📊 Статистика заказов', one_time_keyboard=True)
        btn02 = types.InlineKeyboardButton('Назад', callback_data='Назад', one_time_keyboard=True)
        btn03 = types.InlineKeyboardButton('Отменить заказ', callback_data='Отменить заказ', one_time_keyboard=True)
        btn04 = types.InlineKeyboardButton('Подтвердить выполнение заказа', callback_data='Подтвердить заказ', one_time_keyboard=True)
        btn05 = types.InlineKeyboardButton('Заказ выполнен с браком', callback_data='Заказ с браком', one_time_keyboard=True)

        markup.row(btn01)
        if takeParam2[15] != '':
            markup.row(btn04)
            markup.row(btn05)
            markup.row(btn03)
        markup.row(btn02)

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
        print("все произошло")



@bot1.callback_query_handler(func=lambda callback: callback.data == 'Назад')
def testmess_test(callback):
    message_id = callback.message.message_id
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()

    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()

    if test2[6] == 'True':

        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:

        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
        markup.row(btn02)

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

    # cursor.close()
    # conn.close()



@bot1.callback_query_handler(func=lambda callback: callback.data == 'Назад1')
def testmess_test_test(callback):
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ('%s')" % (take_user_id))
    takeParam2 = cursor.fetchone()
    if takeParam2:
        user_lastname = takeParam2[4]
        user_firstname = takeParam2[5] 
        user_middlename = takeParam2[6]
        user_name = user_lastname + ' ' + user_firstname + ' ' + user_middlename# Предположим, что имя пользователя находится во второй колонке
        print('тут это', user_name)
        print('в админке работает все ', user_name)      
          
        
        application = f'📞 Телефон: +{takeParam2[2]}\n👤 ФИО: {takeParam2[4]} {takeParam2[5]} {takeParam2[6]}\n📅 Дата рождения: {takeParam2[7]}\n🇷🇺 Гражданство РФ: {takeParam2[8]}\n🤝 Самозанятый: {takeParam2[10]} \n🏙 Город(а): {takeParam2[3]}' 


        markup = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='📊 Статистика заказов', one_time_keyboard=True)
        btn02 = types.InlineKeyboardButton('Назад', callback_data='Назад', one_time_keyboard=True)
        btn03 = types.InlineKeyboardButton('Отменить заказ', callback_data='Отменить заказ', one_time_keyboard=True)
        btn04 = types.InlineKeyboardButton('Подтвердить выполнение заказа', callback_data='Подтвердить заказ', one_time_keyboard=True)
        btn05 = types.InlineKeyboardButton('Заказ выполнен с браком', callback_data='Заказ с браком', one_time_keyboard=True)

        markup.row(btn01)
        if takeParam2[15] != '':
            markup.row(btn04)
            markup.row(btn05)
            markup.row(btn03)
        markup.row(btn02)

        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
        print("все произошло")
    cursor.close()
    conn.close()




@bot1.callback_query_handler(func=lambda callback: callback.data == 'Подтвердить заказ') 
def callback_data_of_data_confirm(callback): 
    # global test123

    conn2 = sqlite3.connect('peoplebase.sql')
    cursor2 = conn2.cursor()
    
    cursor2.execute("SELECT actualOrder, orderDone FROM users WHERE id = ('%s')" % (take_user_id))
    takeOrderTake = cursor2.fetchone()

    test_test = takeOrderTake[0]
    
    current_orderId = takeOrderTake[1] if takeOrderTake[1] else ""


    new_orderId = current_orderId + "," + test_test if current_orderId else test_test
    print(new_orderId, 'ТУТ АЛЕ')

    cursor2.execute("UPDATE users SET actualOrder = '%s', orderDone = '%s' WHERE id = '%s'" % ("",  new_orderId, take_user_id))

            
            

    conn2.commit()

    message_id = callback.message.message_id
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()

    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()
    bot1.answer_callback_query(callback.id, "Подтверждение заказа выполнено")


    if test2[6] == 'True':

        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:

        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
        markup.row(btn02)

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    
    # cursor.close()
    # conn.close()

@bot1.callback_query_handler(func=lambda callback: callback.data == 'Заказ с браком') 
def callback_data_of_data_miss(callback): 
    # global test123

    conn2 = sqlite3.connect('peoplebase.sql')
    cursor2 = conn2.cursor()
    
    cursor2.execute("SELECT actualOrder, orderMiss FROM users WHERE id = ('%s')" % (take_user_id))
    takeOrderTake = cursor2.fetchone()

    test_test = takeOrderTake[0]
    
    current_orderId = takeOrderTake[1] if takeOrderTake[1] else ""


    new_orderId = current_orderId + "," + test_test if current_orderId else test_test
    print(new_orderId, 'ТУТ АЛЕ')

    cursor2.execute("UPDATE users SET actualOrder = '%s', orderMiss = '%s' WHERE id = '%s'" % ("",  new_orderId, take_user_id))

            
            

    conn2.commit()

    message_id = callback.message.message_id
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()

    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()

    bot1.answer_callback_query(callback.id, "Заказ был выполнен с браком")


    if test2[6] == 'True':

        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:

        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
        markup.row(btn02)

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    
    # cursor.close()
    # conn.close()
    




@bot1.callback_query_handler(func=lambda callback: callback.data == 'Отменить заказ') 
def callback_data_of_data_close(callback): 
    # global test123

    # conn2 = sqlite3.connect('peoplebase.sql')
    # cursor2 = conn2.cursor()
    
    # cursor2.execute("SELECT actualOrder, orderTake FROM users WHERE id = ('%s')" % (take_user_id))
    # takeOrderTake = cursor2.fetchone()

    # test_test = takeOrderTake[0]
    
    # current_orderId = takeOrderTake[1] if takeOrderTake[1] else ""



    message_id = callback.message.message_id
        

    # # Разделите строку по запятым и удалите последний элемент
    # orderTake_list = current_orderId.split(',')
    # new_orderTake = ','.join(orderTake_list[:-1])


    
    conn_applicationbase = sqlite3.connect('applicationbase.sql')
    cur_applicationbase = conn_applicationbase.cursor()

    # # Замените 'your_peoplebase.sql' на имя вашей базы данных peoplebase.sql
    # conn_peoplebase = sqlite3.connect('peoplebase.sql')
    # cur_peoplebase = conn_peoplebase.cursor()

    user_name_to_remove = callback.from_user.first_name  # Используйте last_name или другие поля, если нужно

    # Поиск соответствующей записи в базе данных applicationbase
    cur_applicationbase.execute("SELECT adminChatId, adminMessageId, whoTakeId FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    order_info = cur_applicationbase.fetchone()

    if order_info:
        admin_chat_id, admin_message_id, who_take_ids_str = order_info
        who_take_ids = who_take_ids_str.split(',') if who_take_ids_str else []

        # Удаление имени пользователя из списка who_take_ids
        if user_name_to_remove in who_take_ids:
            who_take_ids.remove(user_name_to_remove)


        # Обновление базы данных applicationbase с новым списком who_take_ids
        # new_who_take_ids_str = ','.join(who_take_ids)
        print('Я не знаю', who_take_ids)
        cur_applicationbase.execute("UPDATE orders SET whoTakeId = ('%s') WHERE adminMessageId = ('%s')" % (user_name_to_remove, admin_message_id))
        conn_applicationbase.commit()

    conn_applicationbase.close()






    # cursor2.execute("UPDATE users SET actualOrder = '%s', orderTake = '%s' WHERE id = '%s'" % ("",  new_orderTake, take_user_id))

            
            

    # conn2.commit()

    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()

    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()

    bot1.answer_callback_query(callback.id, "Заказ отменен")


    if test2[6] == 'True':

        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:

        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину1', one_time_keyboard=True)
        markup.row(btn02)

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    
    # cursor.close()
    # conn.close()
    




@bot1.callback_query_handler(func=lambda callback: callback.data == '📊 Статистика заказов') 
def callback_data_of_data(callback): 
    global cityTrue
    global isOpenEdit
    global data_called
    global samozanYorN

    global percent_completed
    global percent_failed

    if callback.data == '📊 Статистика заказов':  
        data_called = False         
        conn = sqlite3.connect('peoplebase.sql')
        c = conn.cursor()

        # Выполнение SQL-запроса
        # c.execute("SELECT orderTake, orderDone, orderMiss FROM users")
        c.execute("SELECT * FROM users WHERE id = '%s'" % (take_user_id))
        test2 = c.fetchone()
            # Получение данных
        orderDataTake = test2[16]
        orderDataDone = test2[17]
        orderDataMiss = test2[18] 

        # Разделение данных по запятым и подсчет количества записей
        recordsTake = orderDataTake.split(',')
        orderCountTake = len(recordsTake)

        recordsDone = orderDataDone.split(',')
        orderCountDone = len(recordsDone) - 1

        recordsMiss = orderDataMiss.split(',')
        orderCountMiss = len(recordsMiss) - 1

        print(f"Количество записей: {orderCountTake}")
        print(f"Количество записей: {orderCountDone}")
        print(f"Количество записей: {orderCountMiss}")

        # Закрытие соединения с базой данных
        conn.close()
        try:
            percent_completed = (orderCountDone / (orderCountTake)) * 100
            percent_failed = (orderCountMiss / (orderCountTake)) * 100
        except Exception:
            percent_completed = 0
            percent_failed = 0
            print('на ноль делить нельзя')


        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Назад', callback_data='Назад1', one_time_keyboard=True)

        markup.row(btn02)

        
        bot1.edit_message_text(f'📊 Статистика заказов:\n• Взял: {orderCountTake}\n• Выполнил: {orderCountDone} ({percent_completed}%)\n• Брак: {orderCountMiss} ({percent_failed}%)', callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)





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
    cur.execute(insertIntoBase1 % (cityname, countPeople, adress, whattodo, timetostart, orderTime, salary, adminChatId, sent_message_id, '', 'True', '', '', '', '')) 

    conn.commit()
    cur.close()
    conn.close()    

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {cityname}', url=f'https://t.me/{chatcity}'))

       
    bot1.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    state = 'citizenRU'
    # user_id = get_user_id()
    # print('новый юзер', user_id)
    testMethod()


    start(message)

def show_database_orders(message):
    print(loginin)
    if loginin == True:

        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM orders')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'тут:{el[14]} Чат id: {el[9]}\nЗаявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[8]}, Сообщение админки: {el[10]}, Сообщение ордера: {el[11]}, Id чатов: {el[13]}, записался id: {el[14]}, номера телефонов друзей: {el[15]}, ФИО друзей: {el[16]}\n\n'
        cur.close()
        conn.close()

        bot1.send_message(message.chat.id, info)
        print(info)
    else:
        bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)


def show_database_users(message):
    print(loginin)

    if loginin == True:

        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'Актуальный ордер:{el[15]} и {el[16]} и {el[17]} и {el[18]} \nюзер айди {el[9]}\nПользователь номер: {el[0]}, Дата регистрации: {el[1]}, Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}, Cамозанятость: {el[10]}, Аккаунт подтвержден: {el[11]}, Паспорт: {el[12]}, взял заказ номер: {el[15]} tot {el[17]} \n\n'

        cur.close()
        conn.close()

        bot1.send_message(message.chat.id, info)
        print(info)
    else:
        bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

# def show_database_userOrder(message):
#     print(loginin)
#     if loginin == True:

#         conn = sqlite3.connect('customerBase.sql')
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM orders')
#         users = cur.fetchall()

#         info = ''
#         for el in users:
#             info += f'тут:{el[14]} Чат id: {el[9]}\nЗаявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[8]}, Сообщение админки: {el[10]}, Сообщение ордера: {el[11]}, Id чатов: {el[13]}, записался id: {el[14]}, номера телефонов друзей: {el[15]}, ФИО друзей: {el[16]}\n\n'
#         cur.close()
#         conn.close()

#         bot1.send_message(message.chat.id, info)
#         print(info)
#     else:
#         bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
#         input_admin(message)

print('Bot started')

bot1.polling(non_stop=True)