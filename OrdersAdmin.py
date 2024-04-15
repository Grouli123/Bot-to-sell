import telebot
from telebot import types
import sqlite3
import json
import os.path


# import admin_config.admin_API_key as API_key_one
import admin_config.admin_sqlBase as sqlBase_one
import admin_config.admin_config_message as config_message_one

# import get_orders_config.get_orders_API_key as API_keky_Test



import get_orders_config.get_orders_config_message as config_message_bot_order


import citys.city_list as citys

from SendMessIntoAdmin import SendMessageintoHere

# admin_main.py
# from observable import Observable

# admin_bot = Observable()



# from get_orders_main import testMethod

botApiKey13 = '6433261921:AAEmTi8RVvhuSdYSlxB2uq0x3tP0X4wMRBE'

# arzamasBot = API_key_Test.botAPIArz
# ekaterinburgBot = API_key_Test.botAPIEka
# sankt_peterburgBot = API_key_Test.botAPISan


bot_to_send = None

bot13 = telebot.TeleBot(botApiKey13)
# bot2 = telebot.TeleBot(arzamasBot)
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
offset = 0

test123 = None

# def start(message):    
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     btn2 = types.InlineKeyboardButton(openBaseOrders, callback_data='open_orders')
#     btn3 = types.InlineKeyboardButton(openBasePeople, callback_data='open_people')
#     btn4 = types.InlineKeyboardButton('Открыть базу данных админов', callback_data='open_admin_db')
#     btn5 = types.InlineKeyboardButton('Отображение админов', callback_data='display_admins')
#     markup.add(btn2, btn3, btn4, btn5)
#     bot13.send_message(message.chat.id, startBotMessage, reply_markup=markup)

# def start(message):
#     # Создаем клавиатуру
#     markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
#     # Создаем кнопки
#     btn2 = types.ReplyKeyboardMarkup(openBaseOrders, callback_data='open_orders')
#     btn3 = types.ReplyKeyboardMarkup(openBasePeople, callback_data='open_people')
#     btn4 = types.ReplyKeyboardMarkup('Открыть базу данных админов', callback_data='open_admin_db')
#     btn5 = types.ReplyKeyboardMarkup('Отображение админов', callback_data='display_admins')
#     # Добавляем кнопки в клавиатуру
#     markup.row(btn2, btn3)  # Помещаем первые две кнопки в один ряд
#     markup.row(btn4, btn5)  # Помещаем следующие две кнопки в другой ряд
#     # Отправляем сообщение пользователю с клавиатурой
#     bot13.send_message(message.chat.id, startBotMessage, reply_markup=markup)

# def start(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     btn2 = types.InlineKeyboardButton(openBaseOrders, callback_data=openBaseOrders)
#     btn3 = types.InlineKeyboardButton(openBasePeople, callback_data=openBasePeople)
#     btn4 = types.InlineKeyboardButton('Открыть базу данных админов', callback_data='open_admin_db')
#     btn5 = types.InlineKeyboardButton('Отображение админов', callback_data='Отображение админов')
#     markup.add(btn2, btn3, btn4, btn5)
#     bot13.send_message(message.chat.id, startBotMessage, reply_markup=markup)

def start(message):
    # Создаем клавиатуру
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Создаем кнопки
    btn2 = types.InlineKeyboardButton(openBaseOrders, callback_data='open_orders')
    btn3 = types.InlineKeyboardButton(openBasePeople, callback_data='open_people')
    btn4 = types.InlineKeyboardButton('Открыть базу данных админов', callback_data='open_admin_db')
    btn5 = types.InlineKeyboardButton('Отображение админов', callback_data='display_admins')
    # Добавляем кнопки в клавиатуру
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    # Отправляем сообщение пользователю с клавиатурой
    bot13.send_message(message.chat.id, startBotMessage, reply_markup=markup)





@bot13.message_handler(commands=['start'])
def input_admin(message):      
    global adminChatId
    adminChatId = message.chat.id  # Получаем chat_id из сообщения

    print(loginin)

    if loginin == False:
        bot13.send_message(message.chat.id, 'Введите логин', parse_mode='html')
        bot13.register_next_step_handler(message, admin_check)   
    else:
        start(message)

# @bot13.message_handler(func=lambda message: message.text == 'Отображение админов')
# def display_admins(message):
#     send_customers_keyboard(message)

def admin_check(message):
    if message.text is None:
        bot13.send_message(message.from_user.id, textOnly)
        input_admin(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot13.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_admin(message) 
        else:
            if login == message.text.strip():
                input_password(message)
            else:
                bot13.send_message(message.from_user.id, 'Логин не найден')
                input_admin(message)

def input_password(message):
    bot13.send_message(message.chat.id, 'Введите пароль', parse_mode='html')
    bot13.register_next_step_handler(message, password_check)   

def password_check(message):
    global loginin
    if message.text is None:
        bot13.send_message(message.from_user.id, textOnly)
        input_password(message) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot13.send_message(message.chat.id, adressError)
            message.text.strip(None)
            input_password(message) 
        else:
            if password == message.text.strip():
                loginin = True
                start(message)
            else:
                bot13.send_message(message.from_user.id, 'Пароль не подходит')
                input_password(message)

# def city_of_obj(message):
#     if loginin == True:
#         if message.text is None:
#             bot13.send_message(message.from_user.id, textOnly)
#             start(message) 
#         else:
#             if message.text == openBaseOrders:
#                 bot13.send_message(message.chat.id, openBseOrdersMessage)
#                 show_database_orders(message)
#                 start(message)
#             elif message.text == openBasePeople:
#                 bot13.send_message(message.chat.id, openBasePeopleMessage)
#                 show_database_users(message)
#                 start(message)
#             elif message.text == 'open_admin_db':
#                 bot13.send_message(message.chat.id, 'Открыть базу данных админов')
#                 show_database_userOrder(message)
#                 start(message)
#             # elif message.text == 'Отображение админов':
#             #     bot13.send_message(message.chat.id, 'Отображение админов')
#             #     # send_customers_keyboard(message)
                
#             #     send_customers_keyboard(message)
#             #     start(message)
#             else:
#                 bot13.send_message(message.chat.id, chooseTruePointOfMenu)            
#                 start(message)  
#     else:
#         bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
#         input_admin(message)

# @bot13.message_handler(func=lambda message: message.text == openBaseOrders)
# def handle_open_base_orders(message):
#     # Ваша логика для обработки открытия базы заказов
#     bot13.send_message(message.chat.id, openBseOrdersMessage)
#     show_database_orders(message)

# @bot13.message_handler(func=lambda message: message.text == openBasePeople)
# def handle_open_base_people(message):
#     # Ваша логика для обработки открытия базы людей
#     bot13.send_message(message.chat.id, openBasePeopleMessage)
#     show_database_users(message)

# @bot13.message_handler(func=lambda message: message.text == 'Открыть базу данных админов')
# def handle_open_admin_db(message):
#     # Ваша логика для открытия базы данных админов
#     bot13.send_message(message.chat.id, 'Открыть базу данных админов')
#     show_database_userOrder(message)

# @bot13.message_handler(func=lambda message: message.text == 'Отображение админов')
# def handle_display_admins(message):
#     # Ваша логика для отображения админов
#     send_customers_keyboard(message)
@bot13.callback_query_handler(func=lambda call: call.data == 'open_orders')
def handle_open_base_orders(call):
    bot13.send_message(call.message.chat.id, openBseOrdersMessage)
    show_database_orders(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'open_people')
def handle_open_base_people(call):
    bot13.send_message(call.message.chat.id, openBasePeopleMessage)
    show_database_users(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'open_admin_db')
def handle_open_admin_db(call):
    bot13.send_message(call.message.chat.id, 'Открыть базу данных админов')
    show_database_userOrder(call.message)
    bot13.answer_callback_query(call.id)

        
@bot13.callback_query_handler(func=lambda call: call.data == 'display_admins')
def display_admins(call):
    send_customers_keyboard(call.message)
    bot13.answer_callback_query(call.id)


def send_customers_keyboard(message, page=0):

    conn = sqlite3.connect('custumers.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT last_name, firts_name, middle_name FROM custumers')
    customers = cursor.fetchall()
    conn.close()

    per_page = 10
    start2 = page * per_page
    end = start2 + per_page
    paginated_customers = customers[start2:end]

    keyboard = types.InlineKeyboardMarkup()

    for customer in paginated_customers:
        full_name = ' '.join(customer)
        callback_data = f"show_customer_{customer[0]}"  # Предполагается, что у вас есть уникальный ID или фамилия в customer[0]
        keyboard.add(types.InlineKeyboardButton(full_name, callback_data=callback_data))

    if len(customers) > end:
        keyboard.add(types.InlineKeyboardButton("Вперед", callback_data=f"page_{page+1}"))
    if page > 0:
        keyboard.add(types.InlineKeyboardButton("Назад", callback_data=f"page_{page-1}"))

    bot13.send_message(message.chat.id, "Вот база:", reply_markup=keyboard)

@bot13.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def page_callback(call):
    page = int(call.data.split('_')[1])
    send_customers_keyboard(call.message, page)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data.startswith('show_customer_'))
def show_customer(call):
    last_name = call.data.split('_')[2]
    bot13.send_message(call.message.chat.id, f"Вы выбрали: {last_name}")
    bot13.answer_callback_query(call.id)




def show_database_orders(message):
    print(loginin)
    if loginin == True:
        if not os.path.exists('applicationbase.sql'):
            bot13.send_message(message.chat.id, "База данных пустая")
        else:
            conn = sqlite3.connect('applicationbase.sql')
            cur = conn.cursor()
            cur.execute('SELECT * FROM orders')
            users = cur.fetchall()

            info = ''
            for el in users:
                info += f'тут:{el[14]} Чат id: {el[9]}\nЗаявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[8]}, Сообщение админки: {el[10]}, Сообщение ордера: {el[11]}, Id чатов: {el[13]}, записался id: {el[14]}, номера телефонов друзей: {el[15]}, ФИО друзей: {el[16]}\n\n'
            cur.close()
            conn.close()

            bot13.send_message(message.chat.id, info)
            print(info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def show_database_users(message):
    print(loginin)

    if loginin == True:
        if not os.path.exists('peoplebase.sql'):
            bot13.send_message(message.chat.id, "База данных пустая")
        else:
            conn = sqlite3.connect('peoplebase.sql')
            cur = conn.cursor()

            cur.execute('SELECT * FROM users')
            users = cur.fetchall()

            info = ''
            for el in users:
                info += f'Актуальный ордер:{el[15]} и {el[16]} и {el[17]} и {el[18]} \nюзер айди {el[9]}\nПользователь номер: {el[0]}, Дата регистрации: {el[1]}, Номер телефона: +{el[2]}, Город: {el[3]}, Фамилия: {el[4]}, Имя: {el[5]}, Отчество: {el[6]}, Дата рождения: {el[7]}, Гражданство РФ: {el[8]}, Cамозанятость: {el[10]}, Аккаунт подтвержден: {el[11]}, Паспорт: {el[12]}, взял заказ номер: {el[15]} tot {el[17]} \n\n'

            cur.close()
            conn.close()

            bot13.send_message(message.chat.id, info)
            print(info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def show_database_userOrder(message):
    print(loginin)
    if loginin == True:
        if not os.path.exists('custumers.sql'):
            bot13.send_message(message.chat.id, "База данных пустая")
        else:
            conn = sqlite3.connect('custumers.sql')
            cur = conn.cursor()
            cur.execute('SELECT * FROM custumers')
            users = cur.fetchall()

            info = ''
            for el in users:
                info += f'3:{el[2]} 4:{el[3]} 5:{el[4]} 6:{el[5]} 7:{el[6]} 8:{el[7]} 9:{el[8]} 10:{el[9]}\n\n'
            cur.close()
            conn.close()
            print("Info:", repr(info))  # Добавьте этот отладочный вывод

            bot13.send_message(message.chat.id, info)
            print(info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

print('Bot started')

bot13.polling(non_stop=True)