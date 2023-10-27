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

sent_message_id = None

user_message_ids = {}


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

        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html')
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
    cur.execute(insertIntoBase1 % (cityname, countPeople, adress, whattodo, timetostart, salary, sent_message_id, '', 'True', '', '', '', '')) 

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
            info += f'Заявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[7]}, Сообщение админки: {el[8]}, Сообщение ордера: {el[9]}, Id чатов: {el[11]}, записался id: {el[12]}, номера телефонов друзей: {el[13]}, ФИО друзей: {el[14]}\n\n'
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
            info += f'Пользователь номер: {el[0]}, Дата регистрации: {el[1]}, Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}, Cамозанятость: {el[10]}, Аккаунт подтвержден: {el[11]}, Паспорт: {el[12]}, взял заказ номер: {el[15]} tot {el[16]} {el[17]} \n\n'

        cur.close()
        conn.close()

        bot1.send_message(message.chat.id, info)
        print(info)
    else:
        bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)


print('Bot started')

bot1.polling(non_stop=True)