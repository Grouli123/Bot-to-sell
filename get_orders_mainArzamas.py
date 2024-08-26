import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import time
import re
from SendCloseMessage import SendCloseMessage
import  get_orders_config.get_orders_API_key as API_key
import  get_orders_config.get_orders_config_message as config_message
from apscheduler.schedulers.background import BackgroundScheduler

botApiKey = API_key.botAPIArz

bot = telebot.TeleBot(botApiKey)

bot1 = telebot.TeleBot('6489313384:AAFOdsE5ZTo1pdXL_JNl1lxF_QMRfZ9pE9A')

scheduler = BackgroundScheduler()
scheduler.start()

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

geolocator = None

nuberPhone = None
city = None
lastname = None
firstname = None
middlename = None
dataOfBirth = None       
citizenRF = None
user_id = None

cityTrue = 'False'

check_user_id = None

nalogacc = None
agreeaccaunt = None
passport = None

id_nubmer_list = None

last_sent_message = None
last_message_id = None  

humanCount = None
needText = None

editButtonText1 = 'Сбербанк'
editButtonText2 = 'Тинькофф'
editButtonText3 = 'Другой банк'

error_reported = False  # Флаг для отслеживания, была ли ошибка уже выведена

check_mess_already_send = False

user_last_message_ids = {}

user_message_ids = {}

user_chat_ids = {}

isOpenEdit = False

data_called = False  

samozanYorN = None

orderTake = None
orderDone = None
orderMiss = None

user_id_mess = None
orderTakeTwo = ''

fioFirstFriend = None
fioSecondFriend = None
fioThirdFriend = None

phoneNumberFirstFriend = None
phoneNumberSecondFriend = None
phoneNumberThirdFriend = None

checkThirdFriend = False
checkFourthFriend = False

messageChatId = None

global_user_id = None

test = None

users_who_clicked = []

takeParam2 = None
cardNumber = None

# Определение состояний
STATE_REGISTRATION = 'registration'
STATE_LOCATION = 'location'
STATE_INPUT_LASTNAME = 'input_lastname'
STATE_INPUT_FIRSTNAME = 'input_firstname'
STATE_INPUT_MIDDLENAME = 'input_middlename'
STATE_INPUT_PASSPORT = 'input_passport'
STATE_INPUT_BIRTHDAY = 'input_birthday'
STATE_INPUT_BIRTHDAY2 = 'input_birthday2'
STATE_USER_BIRTHDAY_CHECK = 'user_birthday_check'
STATE_USER_BIRTHDAY_CHECK2 = 'user_birthday_check2'
STATE_READY_PASSPORT_INFO = 'ready_passport_info'
STATE_INPUT_PHONE_NUMBER = 'input_phone_number'
STATE_INPUT_MY_NALOG_ACCOUNT = 'input_my_nalog_account'
STATE_MY_NALOG_ACCOUNT_CHECK = 'my_nalog_account_check'
STATE_DATA = 'data'
STATE_ORDERS = 'orders'
STATE_CALLBACK_DATA_OF_DATA = 'callback_data_of_data'
STATE_CALLBACK_INDIVIDUAL = 'callback_individual'
STATE_CALLBACK_BANK = 'callback_bank'
STATE_CALLBACK_BANK_CHOICE = 'callback_bank_choice'
STATE_CALLBACK_CONTINUE = 'callback_continue'
STATE_CALLBACK_EDIT_PERSON_DATA = 'callback_edit_person_data'
STATE_INPUT_LASTNAME2 = 'input_lastname2'
STATE_LASTNAME_CHECK2 = 'lastname_check2'
STATE_INPUT_FIRSTNAME2 = 'input_firstname2'
STATE_FIRSTNAME_CHECK2 = 'firstname_check2'
STATE_INPUT_MIDDLENAME2 = 'input_middlename2'
STATE_MIDDLENAME_CHECK2 = 'middlename_check2'
STATE_CALLBACK_EDU1 = 'callback_edu1'
STATE_CANCEL_CONFIRMATION = 'cancel_confirmation'
STATE_CALLBACK_RENAME_CITY = 'callback_rename_city'
STATE_CALLBACK_DELETE_CITY = 'callback_delete_city'
STATE_CALLBACK_ADD_CITY = 'callback_add_city'
STATE_LOCATION_CITY_CITIZEN = 'location_city_citizen'
STATE_PASSPORT_CHECK = 'pasport_check'

current_user_id = None

current_user_id = None

# Создаем соединение с базой данных для хранения состояний пользователей
def init_db():
    conn = sqlite3.connect('states.sql')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_states (
                      user_id INTEGER PRIMARY KEY,
                      state TEXT)''')
    conn.commit()
    conn.close()

# Функция для обновления состояния пользователя
def update_state(user_id, state):
    conn = sqlite3.connect('states.sql')
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO user_states (user_id, state) VALUES (?, ?)', (user_id, state))
    conn.commit()
    conn.close()

# Функция для получения текущего состояния пользователя
def get_state(user_id):
    conn = sqlite3.connect('states.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT state FROM user_states WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def insert_user_data(database_name, column, data, user_id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Проверяем, существует ли уже пользователь с данным user_id
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()
    
    if exists:
        # Если пользователь существует, обновляем данные
        cursor.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (data, user_id))
    else:
        # Если пользователя нет, вставляем новую строку с user_id и указанной колонкой
        cursor.execute(f"INSERT INTO users (user_id, {column}) VALUES (?, ?)", (user_id, data))
    
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def registration(message):
    user_id = message.from_user.id

    handle_state(user_id, message)  # Добавляем вызов handle_state
    update_state(user_id, STATE_REGISTRATION)

    try:
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, 'Пользователь не найден')
        return

    try:
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam = cursor.fetchone()
        if takeParam:
            check_user_id = takeParam[9]
        else:
            check_user_id = None

        cursor.execute("UPDATE users SET botChatId = ? WHERE user_id = ?", (message.chat.id, user_id))
        conn.commit()
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, 'Ошибка работы с базой данных.')
        check_user_id = None
    finally:
        cursor.close()
        conn.close()

    if check_user_id:
        bot.send_message(message.chat.id, 'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!')
        update_state(user_id, STATE_ORDER_CONFIRMATION)
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, 'Вы не зарегистрированы, пройдите регистрацию, перейдя к боту по кнопке!', parse_mode='html', reply_markup=markup)

    if check_user_id:
        bot.send_message(message.chat.id, 'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажав на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
        userCitizenRuText = '👉Пока можешь почитать отзывы о нашей организации'
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)
        markup.row(btn3)
        bot.send_message(message.chat.id, userCitizenRuText, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)
        bot.send_message(message.chat.id, 'Вы не зарегистрированы, пройдите регистрацию, перейдя к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_id = message.from_user.id
    handle_state(user_id, message)  # Добавляем вызов handle_state
    
def testMethod():
    global check_mess_already_send
    global check_user_id
    global last_sent_message
    global humanCount
    global needText
    global last_message_id
    global error_reported
    global user_last_message_ids
    global user_message_ids
    global user_chat_ids
    global data_called
    global user_id_mess

    data_called = False
    conn5 = sqlite3.connect('peoplebase.sql')
    cur5 = conn5.cursor()
    cur5.execute("SELECT botChatId FROM users")
    results = cur5.fetchall()
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
        users = cur.fetchone()
        if users is not None and "Арзамас" in users[2]:
            if (int(users[3]) <= 1) or (int(users[3]) >= 5):
                humanCount = 'человек'
            else:
                humanCount = 'человека'
            if int(users[3]) > 1:
                needText = 'Нужно'
            else:
                needText = 'Нужен'

            # Обновляем состояние пользователя
            for result in results:
                user_id = result[0]
                update_state(user_id, STATE_RECEIVED_ORDER)

            # Создаем кнопки в зависимости от количества требуемых людей
            markup2 = types.InlineKeyboardMarkup()
            if int(users[3]) == 1:
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn52)
            elif int(users[3]) == 2:
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn22)
                markup2.row(btn52)
            elif int(users[3]) == 3:
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
                btn32 = types.InlineKeyboardButton('Едем в 3', callback_data='Едем в 3', one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn22)
                markup2.row(btn32)
                markup2.row(btn52)
            elif int(users[3]) >= 4:
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
                btn32 = types.InlineKeyboardButton('Едем в 3', callback_data='Едем в 3', one_time_keyboard=True)
                btn42 = types.InlineKeyboardButton('Едем в 4', callback_data='Едем в 4', one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn22)
                markup2.row(btn32)
                markup2.row(btn42)
                markup2.row(btn52)

            order_info = (f'✅\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n'
                          f'<b>•Адрес:</b>👉 {users[4]}\n'
                          f'<b>•Что делать:</b> {users[5]}\n'
                          f'<b>•Начало работ:</b> в {users[6]}:00\n'
                          f'<b>·Рабочее время:</b> {users[17]}:00\n'
                          f'<b>•Вам на руки:</b> <u>{users[8]}.00</u> р./час, минималка 2 часа\n'
                          f'<b>•Приоритет самозанятым</b>')

            if order_info != last_sent_message:
                user_id_mess = users[0]
                cur.execute("SELECT orderMessageId FROM orders WHERE id = ?", (user_id_mess,))
                current_message_ids_str = cur.fetchone()[0]
                current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []

                for result in results:
                    botChatIdw = result[0]
                    if botChatIdw != 'None':
                        sent_message = bot.send_message(botChatIdw, order_info, reply_markup=markup2, parse_mode='html')
                        last_message_id = sent_message.message_id
                        user_chat_id_str = user_chat_ids.get(user_id_mess, "")
                        if user_chat_id_str:
                            user_chat_id_str += ","
                        user_chat_id_str += str(botChatIdw)
                        user_chat_ids[user_id_mess] = user_chat_id_str
                        user_message_id_list = user_message_ids.get(user_id_mess, [])
                        user_message_id_list.append(last_message_id)
                        user_message_ids[user_id_mess] = user_message_id_list
                        last_message_id_str = str(last_message_id)
                        current_message_ids.append(last_message_id_str)
                        updated_message_ids_str = ','.join(current_message_ids)

                cur5.close()
                conn5.close()

                for user_id_mess, message_id_list in user_message_ids.items():
                    updated_message_ids_str = ','.join(map(str, message_id_list))
                    sql_query = "UPDATE orders SET orderMessageId = ?, orderChatId = ? WHERE id = ?"
                    cur.execute(sql_query, (updated_message_ids_str, user_chat_id_str, user_id_mess))
                conn.commit()
                last_sent_message = order_info
                check_mess_already_send = False
            else:
                print('Нет новых сообщений')
                print(user_last_message_ids)
        else:
            print('Заказов пока нет, но скоро будут')
        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        if not error_reported:
            print('Заказов пока нет, но скоро будут')
            error_reported = True
        conn.close()


def sendNotyfiMessage():
    global check_mess_already_send
    global check_user_id
    global last_sent_message
    global humanCount
    global needText
    global last_message_id
    global error_reported
    global user_last_message_ids
    global user_message_ids
    global user_chat_ids
    global data_called
    global user_id_mess

    data_called = False
    conn5 = sqlite3.connect('peoplebase.sql')
    cur5 = conn5.cursor()
    cur5.execute("SELECT botChatId FROM users")
    results = cur5.fetchall()
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
        users = cur.fetchone()
        if users is not None:
            order_info = f'{users[18]}'

            # Обновляем состояние пользователя
            for result in results:
                user_id = result[0]
                update_state(user_id, STATE_NOTIFICATION_SENT)

            if order_info != last_sent_message:
                user_id_mess = users[0]
                cur.execute("SELECT orderMessageId FROM orders WHERE id = ?", (user_id_mess,))
                current_message_ids_str = cur.fetchone()[0]
                current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []

                for result in results:
                    botChatIdw = result[0]
                    if botChatIdw != 'None':
                        sent_message = bot.send_message(botChatIdw, order_info, parse_mode='html')
                        last_message_id = sent_message.message_id
                        user_chat_id_str = user_chat_ids.get(user_id_mess, "")
                        if user_chat_id_str:
                            user_chat_id_str += ","
                        user_chat_id_str += str(botChatIdw)
                        user_chat_ids[user_id_mess] = user_chat_id_str
                        user_message_id_list = user_message_ids.get(user_id_mess, [])
                        user_message_id_list.append(last_message_id)
                        user_message_ids[user_id_mess] = user_message_id_list
                        last_message_id_str = str(last_message_id)
                        current_message_ids.append(last_message_id_str)
                        updated_message_ids_str = ','.join(current_message_ids)

                cur5.close()
                conn5.close()

                for user_id_mess, message_id_list in user_message_ids.items():
                    updated_message_ids_str = ','.join(map(str, message_id_list))
                    sql_query = "UPDATE orders SET orderMessageId = ?, orderChatId = ? WHERE id = ?"
                    cur.execute(sql_query, (updated_message_ids_str, user_chat_id_str, user_id_mess))
                conn.commit()
                last_sent_message = order_info
                check_mess_already_send = False
            else:
                print('Нет новых сообщений')
                print(user_last_message_ids)
        else:
            print('Заказов пока нет, но скоро будут')
        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        if not error_reported:
            print('Заказов пока нет, но скоро будут')
            error_reported = True
        conn.close()


def update_message_with_users_list(chat_id, message_id, test, user_id, users_who_clicked):
    conn3 = sqlite3.connect('applicationbase.sql')
    cur3 = conn3.cursor()
    cur3.execute("SELECT orderMessageId, adminChatId, adminMessageId FROM orders")
    rows = cur3.fetchall()

    for row in rows:
        order_message_ids = row[0].split(',')
        admin_chat_id = row[1]
        admin_message_id = row[2]

    if str(test) in order_message_ids:
        try:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('Посмотреть запись', callback_data='ОтправленоАдмину')
            btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
            markup.row(btn)
            markup.row(btn01)

            # Обновляем состояние пользователя
            update_state(user_id, STATE_UPDATED_MESSAGE)

            bot1.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_message_id, reply_markup=markup)
        except Exception:
            print('какая-то ошибка, можно игнорировать')

    
@bot.callback_query_handler(func=lambda callback: callback.data == 'Еду 1')
def callback_data_of_data(callback):
    global orderTakeTwo
    global checkThirdFriend
    global checkFourthFriend
    global user_id_mess
    global user_id_name
    global test
    global user_id
    global takeParam2

    if callback.data == 'Еду 1':
        test = callback.message.message_id
        user_id = callback.from_user.id
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (user_id,))
        actual_order = cursor.fetchone()

        if actual_order and actual_order[0] not in [None, ""]:
            bot.send_message(callback.message.chat.id, "Вы уже записаны на заказ")
            conn.close()
            return

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam2 = cursor.fetchone()

        if takeParam2:
            orderTakeTwo = takeParam2[0]
            conn4 = sqlite3.connect('applicationbase.sql')
            cur4 = conn4.cursor()
            cur4.execute("SELECT orderMessageId, id FROM orders")
            rows = cur4.fetchall()
            for row in rows:
                order_message_ids2 = row[0].split(',')
                order_id2 = row[1]

            cur4.close()
            conn4.close()

            users_who_clicked.append(user_id)

            # Обновляем состояние пользователя
            update_state(user_id, STATE_ORDER_CONFIRMED)

            update_message_with_users_list(callback.message.chat.id, callback.message.message_id, test, user_id, users_who_clicked)

            cursor.execute("SELECT orderTake, actualOrder FROM users WHERE user_id = ?", (user_id,))
            takeOrderTake = cursor.fetchone()

            if str(test) in order_message_ids2:
                if takeOrderTake is not None:
                    current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""
                    conn3 = sqlite3.connect('applicationbase.sql')
                    cur3 = conn3.cursor()
                    cur3.execute("SELECT * FROM orders WHERE id = ?", (order_id2,))
                    users = cur3.fetchone()
                    user_id_mess = users[0]
                    cur3.close()
                    conn3.close()
                    new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
                    cursor.execute("UPDATE users SET orderTake = ?, actualOrder = ? WHERE user_id = ?", (new_orderId, str(user_id_mess), user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()

                conn2 = sqlite3.connect('applicationbase.sql')
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT whoTakeId FROM orders WHERE id = ?", (order_id2,))
                current_values = cursor2.fetchone()

                if current_values is not None:
                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo
                    cursor2.execute("UPDATE orders SET whoTakeId = ? WHERE id = ?", (new_phone_numbers, order_id2))
                    conn2.commit()

                cursor2.close()
                conn2.close()

                conn2 = sqlite3.connect('applicationbase.sql')
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT * FROM orders WHERE id = ?", (order_id2,))
                table_element = cursor2.fetchone()

                if table_element is not None:
                    if (int(table_element[3]) <= 1) or (int(table_element[3]) >= 5):
                        humanCount = 'человек'
                    else:
                        humanCount = 'человека'
                    if int(table_element[3]) > 1:
                        needText = 'Нужно'
                    else:
                        needText = 'Нужен'

                order_info = (f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n'
                              f'<b>•Адрес:</b>👉 {table_element[4]}\n'
                              f'<b>•Что делать:</b> {table_element[5]}\n'
                              f'<b>•Начало работ:</b> в {table_element[6]}:00\n'
                              f'<b>•Рабочее время:</b> {table_element[17]}:00\n'
                              f'<b>•Вам на руки:</b> <u>{table_element[8]}.00</u> р./час, минималка 2 часа\n'
                              f'<b>•Приоритет самозанятым</b>')

                bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')
                bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}')
                conn2.commit()
                cursor2.close()
                conn2.close()

                job_time = datetime.strptime(table_element[6], "%H") - timedelta(minutes=20)
                job_time = job_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
                if job_time < datetime.now():
                    job_time = job_time + timedelta(days=1)
                scheduler.add_job(send_reminder, 'date', run_date=job_time, args=[callback.message.chat.id, user_id_mess])


def send_reminder(chat_id, user_id_mess):
    # Обновляем состояние пользователя
    update_state(user_id_mess, STATE_REMINDER_SENT)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data=f'yes_{user_id_mess}'))
    markup.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data=f'close_order_{user_id_mess}'))
    bot.send_message(chat_id, f'Вы выехали на заказ {user_id_mess}?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('yes_') or call.data.startswith('close_order_'))
def handle_reminder_response(call):
    user_id_mess = call.data.split('_')[1]
    
    if call.data.startswith('yes_'):
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ON_THE_WAY)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выехали на заказ {user_id_mess}?')
        send_reminder_two(call.message.chat.id, user_id_mess)
    elif call.data.startswith('close_order_'):
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET actualOrder = '' WHERE user_id = ?", (call.from_user.id,))
        conn.commit()
        cursor.close()
        conn.close()

        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT whoTakeId FROM orders WHERE orderChatId LIKE ?", (f"%{call.message.chat.id}%",))
        result = cursor.fetchone()
        if result:
            who_take_id = result[0]
            updated_who_take_id = ','.join([id for id in who_take_id.split(',') if id != user_id_mess])
            cursor.execute("UPDATE orders SET whoTakeId = ? WHERE orderChatId LIKE ?", (updated_who_take_id, f"%{call.message.chat.id}%"))
            conn.commit()
        cursor.close()
        conn.close()
        
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ORDER_CANCELLED)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы выехали на заказ {user_id_mess}?')
        bot.send_message(call.message.chat.id, 'Заказ отменен.')


def send_reminder_two(chat_id, user_id_mess):
    # Обновляем состояние пользователя
    update_state(user_id_mess, STATE_SECOND_REMINDER_SENT)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data=f'yes2_{user_id_mess}'))
    markup.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data=f'close_order2_{user_id_mess}'))
    bot.send_message(chat_id, f'Вы в пути на заказ {user_id_mess}?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('yes2_') or call.data.startswith('close_order2_'))
def handle_reminder_response_two(call):
    user_id_mess = call.data.split('_')[1]
    
    if call.data.startswith('yes2_'):
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ARRIVED)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы в пути на заказ {user_id_mess}?')
        send_reminder_three(call.message.chat.id, user_id_mess)
    elif call.data.startswith('close_order2_'):
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET actualOrder = '' WHERE user_id = ?", (call.from_user.id,))
        conn.commit()
        cursor.close()
        conn.close()

        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT whoTakeId FROM orders WHERE orderChatId LIKE ?", (f"%{call.message.chat.id}%",))
        result = cursor.fetchone()
        if result:
            who_take_id = result[0]
            updated_who_take_id = ','.join([id for id in who_take_id.split(',') if id != user_id_mess])
            cursor.execute("UPDATE orders SET whoTakeId = ? WHERE orderChatId LIKE ?", (updated_who_take_id, f"%{call.message.chat.id}%"))
            conn.commit()
        cursor.close()
        conn.close()
        
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ORDER_CANCELLED)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы в пути на заказ {user_id_mess}?')
        bot.send_message(call.message.chat.id, 'Заказ отменен.')


def send_reminder_three(chat_id, user_id_mess):
    # Обновляем состояние пользователя
    update_state(user_id_mess, STATE_THIRD_REMINDER_SENT)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data=f'yes3_{user_id_mess}'))
    markup.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data=f'close_order3_{user_id_mess}'))
    bot.send_message(chat_id, f'Вы приехали на заказ {user_id_mess}?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('yes3_') or call.data.startswith('close_order3_'))
def handle_reminder_response_three(call):
    user_id_mess = call.data.split('_')[1]
    
    if call.data.startswith('yes3_'):
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_STARTED_WORK)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы приехали на заказ {user_id_mess}?')
        send_reminder_four(call.message.chat.id, user_id_mess)
    elif call.data.startswith('close_order3_'):
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET actualOrder = '' WHERE user_id = ?", (call.from_user.id,))
        conn.commit()
        cursor.close()
        conn.close()

        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT whoTakeId FROM orders WHERE orderChatId LIKE ?", (f"%{call.message.chat.id}%",))
        result = cursor.fetchone()
        if result:
            who_take_id = result[0]
            updated_who_take_id = ','.join([id for id in who_take_id.split(',') if id != user_id_mess])
            cursor.execute("UPDATE orders SET whoTakeId = ? WHERE orderChatId LIKE ?", (updated_who_take_id, f"%{call.message.chat.id}%"))
            conn.commit()
        cursor.close()
        conn.close()
        
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ORDER_CANCELLED)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы приехали на заказ {user_id_mess}?')
        bot.send_message(call.message.chat.id, 'Заказ отменен.')

def send_reminder_four(chat_id, user_id_mess):
    # Обновляем состояние пользователя
    update_state(user_id_mess, STATE_FINAL_REMINDER_SENT)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data=f'yes4_{user_id_mess}'))
    markup.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data=f'close_order4_{user_id_mess}'))
    bot.send_message(chat_id, f'Вы завершили заказ {user_id_mess}?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('yes4_') or call.data.startswith('close_order4_'))
def handle_reminder_response_four(call):
    user_id_mess = call.data.split('_')[1]
    
    if call.data.startswith('yes4_'):
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (call.from_user.id,))
        actual_order = cursor.fetchone()
        
        if actual_order and actual_order[0] not in [None, ""]:
            cursor.execute("UPDATE users SET orderDone = ?, actualOrder = '' WHERE user_id = ?", (actual_order[0], call.from_user.id))
            conn.commit()
            
            # Обновляем состояние пользователя
            update_state(user_id_mess, STATE_ORDER_COMPLETED)
            
            bot.send_message(call.message.chat.id, 'Отлично! Желаем удачи на заказе.')
        else:
            bot.send_message(call.message.chat.id, 'Нет текущих заказов для завершения.')
        
        cursor.close()
        conn.close()
        
        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT whoTakeId FROM orders WHERE orderChatId LIKE ?", (f"%{call.message.chat.id}%",))
        result = cursor.fetchone()
        
        if result:
            who_take_id = result[0]
            updated_who_take_id = ','.join([id for id in who_take_id.split(',') if id != user_id_mess])
            cursor.execute("UPDATE orders SET whoTakeId = ? WHERE orderChatId LIKE ?", (updated_who_take_id, f"%{call.message.chat.id}%"))
            conn.commit()
        
        cursor.close()
        conn.close()
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы завершили заказ {user_id_mess}?')
        send_reminder_five(call.message)
    elif call.data.startswith('close_order4_'):
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET actualOrder = '' WHERE user_id = ?", (call.from_user.id,))
        conn.commit()
        cursor.close()
        conn.close()

        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT whoTakeId FROM orders WHERE orderChatId LIKE ?", (f"%{call.message.chat.id}%",))
        result = cursor.fetchone()
        
        if result:
            who_take_id = result[0]
            updated_who_take_id = ','.join([id for id in who_take_id.split(',') if id != user_id_mess])
            cursor.execute("UPDATE orders SET whoTakeId = ? WHERE orderChatId LIKE ?", (updated_who_take_id, f"%{call.message.chat.id}%"))
            conn.commit()
        
        cursor.close()
        conn.close()
        
        # Обновляем состояние пользователя
        update_state(user_id_mess, STATE_ORDER_CANCELLED)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вы завершили заказ {user_id_mess}?')
        bot.send_message(call.message.chat.id, 'Заказ отменен.')


def send_reminder_five(message):
    # Обновляем состояние пользователя
    update_state(message.from_user.id, STATE_WAITING_CARD_NUMBER)
    
    bot.send_message(message.chat.id, 'Введите номер карты на которую перевести зарплату за заказ ', parse_mode='html')
    bot.register_next_step_handler(message, send_money_message_admin)


def send_money_message_admin(message):
    global cardNumber
    
    if message.text is None:
        bot.send_message(message.from_user.id, "Пожалуйста, введите текстовое сообщение.")
        return
    
    if len(message.text.strip()) > 20:
        bot.send_message(message.chat.id, "Длина номера карты превышает допустимую.")
        return
    
    cardNumber = message.text.strip()
    
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (message.from_user.id,))
    actual_order = cursor.fetchone()
    
    if actual_order and actual_order[0]:
        cursor.execute("UPDATE users SET orderDone = ?, actualOrder = '' WHERE user_id = ?", (actual_order[0], message.from_user.id))
        conn.commit()
        bot.send_message(message.chat.id, 'Отлично! Желаем удачи на заказе.')
        
        # Обновляем состояние пользователя
        update_state(message.from_user.id, STATE_ORDER_COMPLETED)
    
    cursor.close()
    conn.close()
    
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT adminChatId FROM orders WHERE orderChatId LIKE ?", (f"%{message.chat.id}%",))
    actual_order_admin = cursor.fetchone()
    
    if actual_order_admin:
        SendCloseMessage(int(actual_order_admin[0]), cardNumber, message.from_user.id)
    
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 2') 
def callback_data_of_data_two(callback):     
    global orderTakeTwo
    global user_id_mess
    global test
    global user_id
    global takeParam2

    if callback.data == 'Едем в 2':
        test = callback.message.message_id
        user_id = callback.from_user.id
        
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (user_id,))
        actual_order = cursor.fetchone()
        
        if actual_order and actual_order[0]:
            bot.send_message(callback.message.chat.id, "Вы уже записаны на заказ")
            conn.close()
            return
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam2 = cursor.fetchone()
        
        if takeParam2:
            orderTakeTwo = takeParam2[0]
            
            conn4 = sqlite3.connect('applicationbase.sql')
            cur4 = conn4.cursor()
            cur4.execute("SELECT orderMessageId, id FROM orders")
            rows = cur4.fetchall()
            
            for row in rows:
                order_message_ids2 = row[0].split(',')
                order_id2 = row[1]
            
            cur4.close()
            conn4.close()
        
        conn3 = sqlite3.connect('applicationbase.sql')
        cur3 = conn3.cursor()
        cur3.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        users = cur3.fetchone()
        user_id_mess = users[0]
        cur3.close()
        conn3.close()
        
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        
        cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        table_element = cursor2.fetchone()
        
        if table_element:
            humanCount = 'человек' if (int(table_element[3]) <= 1) or (int(table_element[3]) >= 5) else 'человека'
            needText = 'Нужно' if int(table_element[3]) > 1 else 'Нужен'
        
        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}:00\n<b>•Рабочее время</b> {table_element[17]}:00\n<b>•Вам на руки:</b> <u>{table_element[8]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        
        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')
        conn2.commit()
        
        cursor2.close()
        conn2.close()
        
        input_fio_first_friend(callback.message)
        
        # Обновляем состояние пользователя
        update_state(user_id, STATE_WAITING_FOR_FRIEND_INFO)


@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 3') 
def callback_data_of_data_three(callback):     
    global orderTakeTwo
    global checkThirdFriend
    global user_id_mess
    global test
    global user_id
    global takeParam2

    if callback.data == 'Едем в 3':
        test = callback.message.message_id
        user_id = callback.from_user.id
        
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (user_id,))
        actual_order = cursor.fetchone()
        
        if actual_order and actual_order[0]:
            bot.send_message(callback.message.chat.id, "Вы уже записаны на заказ")
            conn.close()
            return
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam2 = cursor.fetchone()
        
        if takeParam2:
            orderTakeTwo = takeParam2[0]
            
            conn4 = sqlite3.connect('applicationbase.sql')
            cur4 = conn4.cursor()
            cur4.execute("SELECT orderMessageId, id FROM orders")
            rows = cur4.fetchall()
            
            for row in rows:
                order_message_ids2 = row[0].split(',')
                order_id2 = row[1]
            
            cur4.close()
            conn4.close()
        
        conn3 = sqlite3.connect('applicationbase.sql')
        cur3 = conn3.cursor()
        cur3.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        users = cur3.fetchone()
        user_id_mess = users[0]
        cur3.close()
        conn3.close()
        
        checkThirdFriend = True
        
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        
        cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        table_element = cursor2.fetchone()
        
        if table_element:
            humanCount = 'человек' if (int(table_element[3]) <= 1) or (int(table_element[3]) >= 5) else 'человека'
            needText = 'Нужно' if int(table_element[3]) > 1 else 'Нужен'
        
        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}:00\n<b>•Рабочее время</b> {table_element[17]}:00\n<b>•Вам на руки:</b> <u>{table_element[8]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        
        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')
        conn2.commit()
        
        cursor2.close()
        conn2.close()
        
        input_fio_first_friend(callback.message)
        
        # Обновляем состояние пользователя
        update_state(user_id, STATE_WAITING_FOR_FRIEND_INFO)


@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 4') 
def callback_data_of_data_four(callback): 
    global orderTakeTwo
    global checkThirdFriend
    global checkFourthFriend
    global user_id_mess
    global test
    global user_id
    global takeParam2

    if callback.data == 'Едем в 4':
        test = callback.message.message_id
        user_id = callback.from_user.id
        
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT actualOrder FROM users WHERE user_id = ?", (user_id,))
        actual_order = cursor.fetchone()
        
        if actual_order and actual_order[0]:
            bot.send_message(callback.message.chat.id, "Вы уже записаны на заказ")
            conn.close()
            return
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam2 = cursor.fetchone()
        
        if takeParam2:
            orderTakeTwo = takeParam2[0]
            
            conn4 = sqlite3.connect('applicationbase.sql')
            cur4 = conn4.cursor()
            cur4.execute("SELECT orderMessageId, id FROM orders")
            rows = cur4.fetchall()
            
            for row in rows:
                order_message_ids2 = row[0].split(',')
                order_id2 = row[1]
            
            cur4.close()
            conn4.close()
        
        conn3 = sqlite3.connect('applicationbase.sql')
        cur3 = conn3.cursor()
        cur3.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        users = cur3.fetchone()
        user_id_mess = users[0]
        cur3.close()
        conn3.close()
        
        checkThirdFriend = True
        checkFourthFriend = True
        
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        
        cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ?", (test,))
        table_element = cursor2.fetchone()
        
        if table_element:
            humanCount = 'человек' if (int(table_element[3]) <= 1) or (int(table_element[3]) >= 5) else 'человека'
            needText = 'Нужно' if int(table_element[3]) > 1 else 'Нужен'
        
        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}:00\n<b>•Рабочее время</b> {table_element[17]}:00\n<b>•Вам на руки:</b> <u>{table_element[8]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        
        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')
        conn2.commit()
        
        cursor2.close()
        conn2.close()
        
        input_fio_first_friend(callback.message)
        
        # Обновляем состояние пользователя
        update_state(user_id, STATE_WAITING_FOR_FRIEND_INFO)


def input_fio_first_friend(message):
    # Обновляем состояние пользователя на ввод ФИО первого друга
    update_state(message.from_user.id, STATE_INPUT_FIO_FIRST_FRIEND)
    bot.send_message(message.chat.id, 'Введите только ФИО друга', parse_mode='html')
    bot.register_next_step_handler(message, fio_first_friend_check)


def fio_first_friend_check(message):
    global fioFirstFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_fio_first_friend(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_fio_first_friend(message) 
        else:
            fioFirstFriend = message.text.strip()
            print(fioFirstFriend)
            # Обновляем состояние пользователя на ввод номера телефона первого друга
            update_state(message.from_user.id, STATE_INPUT_FIRST_FRIEND_NUMBER)
            input_first_friend_number(message)

def input_first_friend_number(message):
    # Обновляем состояние пользователя на ввод номера телефона первого друга
    update_state(message.from_user.id, STATE_INPUT_FIRST_FRIEND_NUMBER)
    
    bot.send_message(message.chat.id, 'Введите номер телефона друга:', parse_mode='html')
    bot.register_next_step_handler(message, first_friend_number_check)


def first_friend_number_check(message):       
    global phoneNumberFirstFriend
    global checkThirdFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_first_friend_number(message)
    else:
        if len(message.text.strip()) != 11:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона')
            message.text.strip(None)
            input_first_friend_number(message)        
        else:               
            if message.text.isdigit():
                phoneNumberFirstFriend = message.text.strip()    
                if checkThirdFriend is True:          
                    checkThirdFriend = False
                    # Обновляем состояние пользователя на ввод ФИО второго друга
                    update_state(message.from_user.id, STATE_INPUT_FIO_SECOND_FRIEND)
                    input_fio_second_friend(message)           
                    print(checkThirdFriend)
                else:  
                    users_who_clicked.append(user_id)
                    update_message_with_users_list(message.chat.id, message.message_id, test, user_id, users_who_clicked)
                    conn = sqlite3.connect('peoplebase.sql')
                    cursor = conn.cursor()
                    cursor.execute("SELECT orderTake FROM users WHERE user_id = ('%s')" % (user_id))
                    takeOrderTake = cursor.fetchone()
                    if takeOrderTake is not None:
                        current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""                        
                        new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
                        cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (new_orderId, user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    conn2 = sqlite3.connect('applicationbase.sql')
                    cursor2 = conn2.cursor()        
                    cursor2.execute("SELECT whoTakeId FROM orders WHERE id = ('%s')" % (user_id_mess))
                    current_values = cursor2.fetchone()
                    if current_values is not None:
                        current_phone_numbers = current_values[0] if current_values[0] else ""
                        print(type(current_phone_numbers))
                        new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo
                        cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, test))
                    conn2.commit()
                    cursor2.close()
                    conn2.close()
                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()
                    cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE orderMessageId = ('%s')" % (test))
                    current_values = cursor.fetchone()
                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    current_fio = current_values[1] if current_values[1] else ""                    
                    new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend if current_phone_numbers else phoneNumberFirstFriend
                    new_fio = current_fio + "," + fioFirstFriend if current_fio else fioFirstFriend
                    cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, new_fio, test))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    conn4 = sqlite3.connect('peoplebase.sql')
                    cursor4 = conn4.cursor()
                    cursor4.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                    takeOrderTake = cursor4.fetchone()
                    if takeOrderTake is not None:
                        famname = takeOrderTake[4]
                        actualName = takeOrderTake[5]
                        otchName = takeOrderTake[6]
                        userPhone = takeOrderTake[2]
                    cursor4.close()
                    conn4.close()
                    bot.send_message(message.chat.id, f'Вы {famname} {actualName} {otchName} номер телефона: {userPhone} едете с другом: {fioFirstFriend} номер телефона: {phoneNumberFirstFriend}', parse_mode='html')
                    print('Номер телефона друга: ', phoneNumberFirstFriend, 'ФИО друга: ', fioFirstFriend)
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_first_friend_number(message)

def input_fio_second_friend(message):
    # Устанавливаем состояние для ввода ФИО второго друга
    update_state(message.from_user.id, STATE_INPUT_FIO_SECOND_FRIEND)
    
    bot.send_message(message.chat.id, 'Введите только ФИО второго друга', parse_mode='html')
    bot.register_next_step_handler(message, fio_second_friend_check)

def fio_second_friend_check(message):
    global fioSecondFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_fio_second_friend(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            input_fio_second_friend(message)
        else:
            fioSecondFriend = message.text.strip()
            print(fioSecondFriend)
            input_second_friend_number(message)

def input_second_friend_number(message):
    # Устанавливаем состояние для ввода номера телефона второго друга
    update_state(message.from_user.id, STATE_INPUT_SECOND_FRIEND_NUMBER)
    
    bot.send_message(message.chat.id, 'Введите номер телефона второго друга:', parse_mode='html')
    bot.register_next_step_handler(message, second_friend_number_check)

def second_friend_number_check(message):       
    global phoneNumberSecondFriend
    global checkFourthFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_second_friend_number(message)
    else:
        if len(message.text.strip()) != 11:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона')
            input_second_friend_number(message)
        else:               
            if message.text.isdigit():
                phoneNumberSecondFriend = message.text.strip()
                if checkFourthFriend is True:
                    checkFourthFriend = False
                    input_fio_third_friend(message)
                    print(checkFourthFriend)
                else:
                    # Продолжение процесса обработки
                    users_who_clicked.append(user_id)
                    update_message_with_users_list(message.chat.id, message.message_id, test, user_id, users_who_clicked)
                    conn = sqlite3.connect('peoplebase.sql')
                    cursor = conn.cursor()
                    cursor.execute("SELECT orderTake FROM users WHERE user_id = ('%s')" % (user_id))
                    takeOrderTake = cursor.fetchone()
                    if takeOrderTake is not None:
                        current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""
                        new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
                        cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (new_orderId, user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    conn2 = sqlite3.connect('applicationbase.sql')
                    cursor2 = conn2.cursor()
                    cursor2.execute("SELECT whoTakeId FROM orders WHERE orderMessageId = ('%s')" % (test))
                    current_values = cursor2.fetchone()
                    if current_values is not None:
                        current_phone_numbers = current_values[0] if current_values[0] else ""
                        new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo
                        cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, test))
                    conn2.commit()
                    cursor2.close()
                    conn2.close()
                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()
                    cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE orderMessageId = ('%s')" % (test))
                    current_values = cursor.fetchone()
                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    current_fio = current_values[1] if current_values[1] else ""
                    new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend + "," + phoneNumberSecondFriend if current_phone_numbers else phoneNumberFirstFriend + "," + phoneNumberSecondFriend
                    new_fio = current_fio + "," + fioFirstFriend + "," + fioSecondFriend if current_fio else fioFirstFriend + "," + fioSecondFriend
                    cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, new_fio, test))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    conn4 = sqlite3.connect('peoplebase.sql')
                    cursor4 = conn4.cursor()
                    cursor4.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                    takeOrderTake = cursor4.fetchone()
                    if takeOrderTake is not None:
                        famname = takeOrderTake[4]
                        actualName = takeOrderTake[5]
                        otchName = takeOrderTake[6]
                        userPhone = takeOrderTake[2]
                    cursor4.close()
                    conn4.close()
                    bot.send_message(message.chat.id, f'Вы {famname} {actualName} {otchName} номер телефона: {userPhone}.\nВаши друзья:\n1. {fioFirstFriend} номер телефона: {phoneNumberFirstFriend}\n2. {fioSecondFriend} номер телефона: {phoneNumberSecondFriend}', parse_mode='html')
                    print('Номер телефона друга: ', phoneNumberSecondFriend, 'ФИО друга: ', fioSecondFriend)
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_second_friend_number(message)

def input_fio_third_friend(message):
    # Устанавливаем состояние для ввода ФИО третьего друга
    update_state(message.from_user.id, STATE_INPUT_FIO_THIRD_FRIEND)
    
    bot.send_message(message.chat.id, 'Введите только ФИО третьего друга', parse_mode='html')
    bot.register_next_step_handler(message, fio_third_friend_check)

def fio_third_friend_check(message):
    global fioThirdFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_fio_third_friend(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            input_fio_third_friend(message)
        else:
            fioThirdFriend = message.text.strip()
            print(fioThirdFriend)
            input_third_friend_number(message)

def input_third_friend_number(message):
    # Устанавливаем состояние для ввода номера телефона третьего друга
    update_state(message.from_user.id, STATE_INPUT_THIRD_FRIEND_NUMBER)
    
    bot.send_message(message.chat.id, 'Введите номер телефона третьего друга:', parse_mode='html')
    bot.register_next_step_handler(message, third_friend_number_check)

def third_friend_number_check(message):   
    global phoneNumberThirdFriend
    # Устанавливаем состояние для проверки номера телефона третьего друга
    update_state(message.from_user.id, STATE_THIRD_FRIEND_NUMBER_CHECK)

    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_third_friend_number(message)
    else:
        if len(message.text.strip()) != 11:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона')
            input_third_friend_number(message)
        else:               
            if message.text.isdigit():
                phoneNumberThirdFriend = message.text.strip()
                users_who_clicked.append(user_id)
                update_message_with_users_list(message.chat.id, message.message_id, test, user_id, users_who_clicked)
                conn = sqlite3.connect('peoplebase.sql')
                cursor = conn.cursor()
                cursor.execute("SELECT orderTake FROM users WHERE user_id = ('%s')" % (user_id))
                takeOrderTake = cursor.fetchone()
                if takeOrderTake is not None:
                    current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""
                    new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
                    cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (new_orderId, user_id))
                conn.commit()
                cursor.close()
                conn.close()
                
                conn2 = sqlite3.connect('applicationbase.sql')
                cursor2 = conn2.cursor()        
                cursor2.execute("SELECT whoTakeId FROM orders WHERE orderMessageId = ('%s')" % (test))
                current_values = cursor2.fetchone()
                print(user_id_mess)
                if current_values is not None:
                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo
                    cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, test))
                conn2.commit()
                cursor2.close()
                conn2.close()
                
                conn = sqlite3.connect('applicationbase.sql')
                cursor = conn.cursor()
                cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE orderMessageId = ('%s')" % (test))
                current_values = cursor.fetchone()
                current_phone_numbers = current_values[0] if current_values[0] else ""
                current_fio = current_values[1] if current_values[1] else ""
                new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend + "," + phoneNumberSecondFriend + "," + phoneNumberThirdFriend if current_phone_numbers else phoneNumberFirstFriend + "," + phoneNumberSecondFriend + "," + phoneNumberThirdFriend
                new_fio = current_fio + "," + fioFirstFriend + "," + fioSecondFriend + "," + fioThirdFriend if current_fio else fioFirstFriend + "," + fioSecondFriend + "," + fioThirdFriend
                cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, new_fio, test))
                conn.commit()
                cursor.close()
                conn.close()
                
                conn4 = sqlite3.connect('peoplebase.sql')
                cursor4 = conn4.cursor()
                cursor4.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                takeOrderTake = cursor4.fetchone()
                if takeOrderTake is not None:
                    famname = takeOrderTake[4]
                    actualName = takeOrderTake[5]
                    otchName = takeOrderTake[6]
                    userPhone = takeOrderTake[2]
                cursor4.close()
                conn4.close()
                
                bot.send_message(message.chat.id, f'Вы {famname} {actualName} {otchName} номер телефона: {userPhone}.\nВаши друзья:\n1.{fioFirstFriend} номер телефона: {phoneNumberFirstFriend}\n2. {fioSecondFriend} номер телефона: {phoneNumberSecondFriend}\n3. {fioThirdFriend} номер телефона: {phoneNumberThirdFriend}', parse_mode='html')
                print('Номер телефона друга: ', phoneNumberFirstFriend, 'ФИО друга: ', fioFirstFriend)
                print('Номер телефона друга: ', phoneNumberSecondFriend, 'ФИО друга: ', fioSecondFriend)
                print('Номер телефона друга: ', phoneNumberThirdFriend, 'ФИО друга: ', fioThirdFriend)
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_third_friend_number(message)

@bot.message_handler(commands=['data'])
def data(message):
    user_id = message.from_user.id
    handle_state(user_id, message)  # Добавляем вызов handle_state
    # Устанавливаем состояние для обработки команды /data
    update_state(message.from_user.id, STATE_DATA)
    
    global user_id, city, cityTrue, nuberPhone, lastname, firstname, middlename, dataOfBirth       
    global citizenRF, id_nubmer_list, check_user_id, data_called, nalogacc, passport
    global samozanYorN, orderTake, orderDone, orderMiss, percent_completed, percent_failed    

    user_id = message.from_user.id

    if not data_called:
        try:
            conn = sqlite3.connect('peoplebase.sql')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            takeParam = cursor.fetchone() 
            if takeParam:
                check_user_id = takeParam[9]
            else:
                check_user_id = None
            conn.close()
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, "Вы еще не взяли ни одного заказа")
            return

        if takeParam:
            id_nubmer_list = takeParam[0]
            nuberPhone = takeParam[2]
            city = takeParam[3]
            lastname = takeParam[4]
            firstname = takeParam[5]
            middlename = takeParam[6]
            dataOfBirth = takeParam[7]        
            citizenRF = takeParam[8]   
            cityTrue = takeParam[14]  
            nalogacc = takeParam[10]  
            passport = takeParam[12]
            orderTake = takeParam[15]
            orderDone = takeParam[16]
            orderMiss = takeParam[17]
        else:
            bot.send_message(message.chat.id, "Пользователь не найден в базе данных.")
            return

        if nalogacc == 'Нет':
            samozanYorN = 'Нет'
        elif passport != 'Нет':
            samozanYorN = f'Да\n💰 Р/С: {nalogacc}\n🪪 Паспорт: {passport}'
        else:
            samozanYorN = f'Да\n💰 Р/С: {nalogacc}'

        if check_user_id is not None or user_id is not None:
            if cityTrue == 'False':
                markup = types.InlineKeyboardMarkup()
                btn2 = types.InlineKeyboardButton('🖌Редактировать город', callback_data='🖌Редактировать город', one_time_keyboard=True)
                btn3 = types.InlineKeyboardButton('✅Подтвердить', callback_data='✅Подтвердить', one_time_keyboard=True)
                markup.row(btn2)  
                markup.row(btn3)  
                bot.send_message(message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN} \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить', reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('📝Редактировать данные', callback_data='📝Редактировать данные', one_time_keyboard=True)
                btn2 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='📊 Статистика заказов', one_time_keyboard=True)
                markup.row(btn1)  
                markup.row(btn2)  
                if passport == 'Нет':
                    messageInformation = f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN}\n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить'
                    btn3 = types.InlineKeyboardButton('✅Подтвердить аккаунт', callback_data='✅Подтвердить аккаунт', one_time_keyboard=True)
                    markup.row(btn3)  
                else:
                    messageInformation = f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN}\n🏙 Город(а): {city}'
                if nalogacc == 'Нет':
                    btn4 = types.InlineKeyboardButton('✅Самозанятость', callback_data='✅Самозанятость', one_time_keyboard=True)
                    markup.row(btn4)  
                bot.send_message(message.chat.id, messageInformation, reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
            markup.row(btn2)          
            bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)

        data_called = True  
    else:
        bot.send_message(message.chat.id, 'Функция data уже была вызвана. Повторный вызов невозможен.')

@bot.message_handler(commands=['orders'])
def orders(message):
    user_id = message.from_user.id
    handle_state(user_id, message)  # Добавляем вызов handle_state
    # Устанавливаем состояние для обработки команды /orders
    update_state(message.from_user.id, STATE_ORDERS)
    
    global check_user_id
    global data_called
    data_called = False    
    user_id = message.from_user.id

    try:
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        takeParam = cursor.fetchone() 
        if takeParam:
            check_user_id = takeParam[15]
        else:
            check_user_id = None
        conn.close()
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, "Пользователь не найден ")
        return

    if check_user_id is not None or user_id is not None:
        try:
            conn = sqlite3.connect('applicationbase.sql')
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE id = ?", (check_user_id,))
            users = cur.fetchall()
            if users:
                info = ''
                for el in users:
                    info += (f'Вы взяли заказ номер: {el[0]}\n'
                             f'<b>•Город:</b> {el[2]}\n'
                             f'<b>•Адрес:</b>👉 {el[4]}\n'
                             f'<b>•Что делать:</b> {el[5]}\n'
                             f'<b>•Начало работ:</b> в {el[6]}:00\n'
                             f'<b>•Рабочее время</b> {el[17]}:00\n'
                             f'<b>•Вам на руки:</b> <u>{el[8]}.00</u> р./час, минималка 2 часа\n'
                             f'<b>•Приоритет самозанятым</b>')
                bot.send_message(message.chat.id, info, parse_mode='html')
            else:
                bot.send_message(message.chat.id, "Заказы не найдены.")
            cur.close()
            conn.close()
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, "Вы еще не взяли ни одного заказа")
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, 'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)

def input_birtgday(message):
    # Устанавливаем состояние для ввода даты рождения
    update_state(message.from_user.id, STATE_INPUT_BIRTHDAY)
    
    if isOpenEdit == True:
        bot.send_message(message.chat.id, dataOfBirthday, parse_mode='html')
        bot.register_next_step_handler(message, user_birthday_check)
    else:
        data(message)

def get_date(text):
    try:
        date = datetime.strptime(text, dateType)
        return date.strftime(dateType)
    except ValueError:
        return None
def user_birthday_check(message):
    global dataOfBirth
    # Устанавливаем состояние для проверки даты рождения пользователя
    update_state(message.from_user.id, STATE_USER_BIRTHDAY_CHECK)
    
    if isOpenEdit == True:
        try:
            if message.text is None:
                bot.send_message(message.from_user.id, textOnly)
                input_birtgday(message)
            else:
                dataOfBirth = get_date(message.text.strip())
                if dataOfBirth:
                    print('OP')
                else:
                    bot.send_message(message.chat.id, dateError)
                    bot.register_next_step_handler(message, user_birthday_check)
        except ValueError:
            bot.send_message(message.chat.id, dateError)
            bot.register_next_step_handler(message, user_birthday_check)
    else:
        data(message)

def input_birtgday2(message):
    # Устанавливаем состояние для ввода второй даты рождения
    update_state(message.from_user.id, STATE_INPUT_BIRTHDAY2)
    
    if isOpenEdit == True:
        bot.send_message(message.chat.id, dataOfBirthday, parse_mode='html')
        bot.register_next_step_handler(message, user_birthday_check2)
    else:
        data(message)

def get_date2(text):
    try:
        date = datetime.strptime(text, dateType)
        return date.strftime(dateType)
    except ValueError:
        return None

def user_birthday_check2(message):
    global dataOfBirth
    # Устанавливаем состояние для второй проверки даты рождения
    update_state(message.from_user.id, STATE_USER_BIRTHDAY_CHECK2)
    
    if isOpenEdit == True:
        try:
            if message.text is None:
                bot.send_message(message.from_user.id, textOnly)
                input_birtgday2(message)
            else:
                dataOfBirth = get_date2(message.text.strip())
                if dataOfBirth:
                    readyPassportInfo(message)
                else:
                    bot.send_message(message.chat.id, dateError)
                    bot.register_next_step_handler(message, user_birthday_check2)
        except ValueError:
            bot.send_message(message.chat.id, dateError)
            bot.register_next_step_handler(message, user_birthday_check2)
    else:
        data(message)

@bot.callback_query_handler(func=lambda callback: callback.data == '📝Редактировать данные' or 
                                                callback.data == '📊 Статистика заказов' or 
                                                callback.data == '✅Подтвердить аккаунт' or 
                                                callback.data == '✅Самозанятость')
def callback_data_of_data(callback):
    global cityTrue, isOpenEdit, data_called, samozanYorN, percent_completed, percent_failed
    # Устанавливаем состояние для обработки callback
    update_state(callback.from_user.id, STATE_CALLBACK_DATA_OF_DATA)

    if callback.data == '📝Редактировать данные':
        data_called = False
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cityTrue = 'False'
        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET cityAgree = '%s' WHERE id = '%s'" % (cityTrue, id_nubmer_list))
        conn.commit()
        cur.close()
        conn.close()
        print('сити тру ', cityTrue)
        data(callback.message)
    elif callback.data == '📊 Статистика заказов':
        data_called = False
        conn = sqlite3.connect('peoplebase.sql')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = '%s'" % (id_nubmer_list))
        test2 = c.fetchone()
        orderDataTake = test2[16]
        orderDataDone = test2[17]
        orderDataMiss = test2[18]
        recordsTake = orderDataTake.split(',')
        orderCountTake = len(recordsTake)
        recordsDone = orderDataDone.split(',')
        orderCountDone = len(recordsDone) - 1
        recordsMiss = orderDataMiss.split(',')
        orderCountMiss = len(recordsMiss) - 1
        print(f"Количество записей: {orderCountTake}")
        print(f"Количество записей: {orderCountDone}")
        print(f"Количество записей: {orderCountMiss}")
        conn.close()
        try:
            percent_completed = (orderCountDone / orderCountTake) * 100
            percent_failed = (orderCountMiss / orderCountTake) * 100
        except Exception:
            percent_completed = 0
            percent_failed = 0
            print('на ноль делить нельзя')
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, f'📊 Статистика заказов:\n• Взял: {orderCountTake}\n• Выполнил: {orderCountDone} ({percent_completed}%)\n• Брак: {orderCountMiss} ({percent_failed}%)', reply_markup=markup)
    elif callback.data == '✅Подтвердить аккаунт':
        print(nuberPhone, lastname)
        data_called = False
        isOpenEdit = True
        bot.edit_message_text(f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN} \n🏙 Город(а): {city}', callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)
        input_lastname(callback.message)
    elif callback.data == '✅Самозанятость':
        data_called = False
        bot.edit_message_text(f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN} \n🏙 Город(а): {city}', callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Кто такой самозанятый❓', callback_data='Кто такой самозанятый❓', one_time_keyboard=True, url='https://npd.nalog.ru/')
        btn2 = types.InlineKeyboardButton('✅Да, официально зарегистрирован', callback_data='✅Да, официально зареган', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('☑️ Нет, хочу зарегистрироваться', callback_data='☑️ Нет, хочу зарегистрироваться', one_time_keyboard=True)
        btn4 = types.InlineKeyboardButton('➡️ Нет, пропустить', callback_data='➡️ Нет, пропустить', one_time_keyboard=True)
        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)
        bot.send_message(callback.message.chat.id, f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Да, официально зареган' or 
                                                callback.data == '☑️ Нет, хочу зарегистрироваться' or 
                                                callback.data == '➡️ Нет, пропустить')
def callback_individual(callback):
    global editButtonText1, editButtonText2, editButtonText3
    # Устанавливаем состояние для обработки индивидуальных callback
    update_state(callback.from_user.id, STATE_CALLBACK_INDIVIDUAL)

    editButtonText1 = 'Сбербанк'
    editButtonText2 = 'Тинькофф'
    editButtonText3 = 'Другой банк'
    if callback.data == '☑️ Нет, хочу зарегистрироваться':
        bot.edit_message_text(f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)
        markup.row(btn1, btn2, btn3)
        bot.send_message(callback.message.chat.id, f'🏦 Каким банком пользуешься?', reply_markup=markup)
    elif callback.data == '➡️ Нет, пропустить':
        bot.edit_message_text(f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', callback.message.chat.id, callback.message.message_id)
    elif callback.data == '✅Да, официально зареган':
        bot.edit_message_text(f'1. Самозанятые грузчики имеют самый большой приоритет при назначении на заявку.\n2. Получают выплаты с минимальной задержкой.\n3. У вас будет официальный доход, налоги мы берём на себя.\n\n✅ Официально зарегистрирован как самозанятый🤝?', callback.message.chat.id, callback.message.message_id)
        input_my_nalog_accaunt(callback.message)

def input_my_nalog_accaunt(message):
    # Устанавливаем состояние для ввода налогового счета
    update_state(message.from_user.id, STATE_INPUT_MY_NALOG_ACCOUNT)
    
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('➡️ Пропустить', callback_data='➡️ Пропустить2', one_time_keyboard=True)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, my_nalog_accaunt_check)
def my_nalog_accaunt_check(message):
    global nalogacc
    # Устанавливаем состояние для проверки налогового счета
    update_state(message.from_user.id, STATE_MY_NALOG_ACCOUNT_CHECK)

    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_my_nalog_accaunt(message) 
    else:
        if len(message.text.strip()) != 20:
            bot.send_message(message.chat.id, 'Введите корректный номер счета')
            input_my_nalog_accaunt(message) 
        else:
            if message.text.isdigit():
                bot.edit_message_text(f'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', message.chat.id, message.message_id-1)
                nalogacc = message.text.strip()
                print(nalogacc)
                conn = sqlite3.connect('peoplebase.sql')
                cur = conn.cursor()
                cur.execute("UPDATE users SET samozanatost = '%s' WHERE id = '%s'" % (nalogacc, id_nubmer_list))
                conn.commit() 
                cur.close()
                conn.close()
                bot.send_message(message.chat.id, f'✅ Самозанятость подтверждена.\nСчет: {nalogacc}')
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер счета')
                input_my_nalog_accaunt(message) 

@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Пропустить2')
def callback_bank(callback):
    # Устанавливаем состояние для обработки callback на пропуск
    update_state(callback.from_user.id, STATE_CALLBACK_BANK)

    if callback.data == '➡️ Пропустить2': 
        bot.edit_message_text(f'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', callback.message.chat.id, callback.message.message_id)
        data(callback.message)

@bot.callback_query_handler(func=lambda callback: callback.data in [editButtonText1, editButtonText2, editButtonText3])
def callback_bank(callback): 
    global editButtonText1, editButtonText2, editButtonText3
    # Устанавливаем состояние для выбора банка
    update_state(callback.from_user.id, STATE_CALLBACK_BANK_CHOICE)

    if callback.data == editButtonText1:
        editButtonText1 = '✅ Сбербанк'
        editButtonText2 = 'Тинькофф'
        editButtonText3 = 'Другой банк'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)  
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)        
        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'Инструкция для Сбербанк...', callback.message.chat.id, callback.message.message_id, reply_markup=markup)   
    elif callback.data == editButtonText2:
        editButtonText2 = '✅Тинькофф'        
        editButtonText1 = 'Сбербанк'
        editButtonText3 = 'Другой банк'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True)        
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)     
        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'Инструкция для Тинькофф...', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == editButtonText3:
        editButtonText3 = '✅Другой банк'
        editButtonText1 = 'Сбербанк'
        editButtonText2 = 'Тинькофф'
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(editButtonText1, callback_data=editButtonText1, one_time_keyboard=True)
        btn2 = types.InlineKeyboardButton(editButtonText2, callback_data=editButtonText2, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(editButtonText3, callback_data=editButtonText3, one_time_keyboard=True) 
        btn4 = types.InlineKeyboardButton('➡️ Продолжить', callback_data='➡️ Продолжить', one_time_keyboard=True)            
        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.edit_message_text(f'Инструкция для Другого банка...', callback.message.chat.id, callback.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Продолжить')
def callback_edit_data_person(callback):
    # Устанавливаем состояние для продолжения после выбора банка
    update_state(callback.from_user.id, STATE_CALLBACK_CONTINUE)

    if callback.data == '➡️ Продолжить':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

@bot.callback_query_handler(func=lambda callback: callback.data in ['🖌Редактировать ФИО', '🖌Редактировать ДР', '🖌Редактировать ПС', '✅ Подтвердить', '➡️ Пропустить'])
def callback_edit_person_data_alone(callback):
    global agreeaccaunt, isOpenEdit
    # Устанавливаем состояние для редактирования данных пользователя
    update_state(callback.from_user.id, STATE_CALLBACK_EDIT_PERSON_DATA)

    if callback.data == '🖌Редактировать ФИО':
        isOpenEdit = True
        input_lastname2(callback.message)
    elif callback.data == '🖌Редактировать ДР':
        isOpenEdit = True
        input_birtgday2(callback.message)
    elif callback.data == '🖌Редактировать ПС':
        isOpenEdit = True
        input_passport(callback.message)
    elif callback.data == '✅ Подтвердить':
        agreeaccaunt = 'Подтвержден'
        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET last_name = '%s', firts_name = '%s', middle_name = '%s', birthday = '%s', agreeacc = '%s', passport = '%s' WHERE id = '%s'" % (lastname, firstname, middlename, dataOfBirth, agreeaccaunt, passport, id_nubmer_list))
        conn.commit() 
        cur.close()
        conn.close()
        bot.answer_callback_query(callback_query_id=callback.id, text='Аккаунт подтвержден')        
        bot.edit_message_text(f'✅ Данные подтверждены\nФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', callback.message.chat.id, callback.message.message_id, parse_mode='html')
    elif callback.data == '➡️ Пропустить':
        bot.edit_message_text(f'ФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', callback.message.chat.id, callback.message.message_id, parse_mode='html')

def input_lastname2(message):
    # Устанавливаем состояние для ввода фамилии
    update_state(message.from_user.id, STATE_INPUT_LASTNAME2)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, 'Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, lastneme_check2)   
    else:
        data(message)

def lastneme_check2(message):
    global lastname
    # Устанавливаем состояние для проверки фамилии
    update_state(message.from_user.id, STATE_LASTNAME_CHECK2)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_lastname2(message) 
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, lastnameError)
                input_lastname2(message) 
            else:
                lastname = message.text.strip()
                print(lastname)
                bot.edit_message_text('Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                input_firstname2(message)
    else:
        data(message)
def input_firstname2(message):
    # Устанавливаем состояние для ввода имени
    update_state(message.from_user.id, STATE_INPUT_FIRSTNAME2)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО имя как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, firstname_check2)
    else:
        data(message)

def firstname_check2(message):       
    global firstname
    # Устанавливаем состояние для проверки имени
    update_state(message.from_user.id, STATE_FIRSTNAME_CHECK2)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_firstname2(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, firstnameError)
                input_firstname2(message)        
            else:                  
                firstname = message.text.strip()    
                print(firstname)
                bot.edit_message_text('🖌Введи ТОЛЬКО имя как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                input_middlename2(message)
    else:
        data(message)

def input_middlename2(message):
    # Устанавливаем состояние для ввода отчества
    update_state(message.from_user.id, STATE_INPUT_MIDDLENAME2)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО отчество как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, middlename_check2)
    else:
        data(message)

def middlename_check2(message):      
    global middlename
    # Устанавливаем состояние для проверки отчества
    update_state(message.from_user.id, STATE_MIDDLENAME_CHECK2)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_middlename2(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, middlenameError)
                input_middlename2(message) 
            else:     
                middlename = message.text.strip()
                print(middlename)
                bot.edit_message_text('🖌Введи ТОЛЬКО отчество как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                readyPassportInfo(message)
    else:
        data(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'Еду1')
def callback_data_of_data(callback):
    # Устанавливаем состояние для обработки callback 'Еду1'
    update_state(callback.from_user.id, STATE_CALLBACK_EDU1)

    if callback.data == 'Еду1':
        bot.send_message(callback.message.chat.id, 'Все работает', parse_mode='html')

@bot.callback_query_handler(func=lambda callback: callback.data == '❌ Отменить подтверждение')
def callback_delete_previos_message(callback):
    global isOpenEdit
    # Устанавливаем состояние для отмены подтверждения
    update_state(callback.from_user.id, STATE_CANCEL_CONFIRMATION)

    if callback.data == '❌ Отменить подтверждение':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        isOpenEdit = False

def input_lastname(message):
    # Устанавливаем состояние для ввода фамилии
    update_state(message.from_user.id, STATE_INPUT_LASTNAME)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, 'Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, lastneme_check)   
    else:
        data(message)

def lastneme_check(message):
    global lastname
    # Устанавливаем состояние для проверки фамилии
    update_state(message.from_user.id, STATE_LASTNAME_CHECK)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_lastname(message) 
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, lastnameError)
                input_lastname(message) 
            else:
                lastname = message.text.strip()
                print(lastname)
                bot.edit_message_text('Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', message.chat.id, message.message_id - 1,  parse_mode='html')
                input_firstname(message)
    else:
        data(message)

def input_firstname(message):
    # Устанавливаем состояние для ввода имени
    update_state(message.from_user.id, STATE_INPUT_FIRSTNAME)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО имя как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, firstname_check)
    else:
        data(message)

def firstname_check(message):       
    global firstname
    # Устанавливаем состояние для проверки имени
    update_state(message.from_user.id, STATE_FIRSTNAME_CHECK)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_firstname(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, firstnameError)
                input_firstname(message)        
            else:                  
                firstname = message.text.strip()    
                print(firstname)
                bot.edit_message_text('🖌Введи ТОЛЬКО имя как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                input_middlename(message)
    else:
        data(message)

def input_middlename(message):
    # Устанавливаем состояние для ввода отчества
    update_state(message.from_user.id, STATE_INPUT_MIDDLENAME)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, '🖌Введи ТОЛЬКО отчество как в паспорте:', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, middlename_check)
    else:
        data(message)
def middlename_check(message):      
    global middlename
    # Устанавливаем состояние для проверки отчества
    update_state(message.from_user.id, STATE_MIDDLENAME_CHECK)

    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_middlename(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, middlenameError)
                input_middlename(message) 
            else:     
                middlename = message.text.strip()
                print(middlename)
                bot.edit_message_text('🖌Введи ТОЛЬКО отчество как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                input_passport(message)
    else:
        data(message)

def input_passport(message):
    # Устанавливаем состояние для ввода паспорта
    update_state(message.from_user.id, STATE_INPUT_PASSPORT)

    if isOpenEdit == True:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, 'ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, passport_check)
    else:
        data(message)

def passport_check(message):      
    global passport
    # Устанавливаем состояние для проверки паспорта
    update_state(message.from_user.id, STATE_PASSPORT_CHECK)

    if isOpenEdit == True:
        if message.text is None:
            bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')
            bot.send_message(message.from_user.id, 'Введите цифры')
            input_passport(message)
        else:
            if len(message.text.strip()) != 10:
                bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')
                bot.send_message(message.chat.id, 'Введите цифры')
                input_passport(message)     
            else:
                if message.text.isdigit():
                    passport = message.text.strip()
                    print(passport)
                    bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')
                    readyPassportInfo(message)
                else:
                    bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')
                    bot.send_message(message.from_user.id, 'Введите цифры')
                    input_passport(message)
    else:
        data(message)

def readyPassportInfo(message):
    # Устанавливаем состояние для подготовки информации о паспорте
    update_state(message.from_user.id, STATE_READY_PASSPORT_INFO)

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🖌Редактировать ФИО', callback_data='🖌Редактировать ФИО', one_time_keyboard=True)
    btn2 = types.InlineKeyboardButton('🖌Редактировать дату рождения', callback_data='🖌Редактировать ДР', one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton('🖌Редактировать паспорт', callback_data='🖌Редактировать ПС', one_time_keyboard=True)        
    btn4 = types.InlineKeyboardButton('✅ Подтвердить(Осталось попыток:2)', callback_data='✅ Подтвердить', one_time_keyboard=True)
    btn5 = types.InlineKeyboardButton('➡️ Пропустить, остаться с низким приоритетом', callback_data='➡️ Пропустить', one_time_keyboard=True)
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)
    markup.row(btn5)
    bot.send_message(message.chat.id, f'Введите верные данные паспорта (фио/дата рождения/серия+номер)\n\nФИО: {lastname} {firstname} {middlename}\n\nДата рождения: {dataOfBirth}\n\nСерия и номер паспорта: {passport}', parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать город')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Подтвердить') 
def callback_rename_city(callback):
    # Устанавливаем состояние для редактирования города или подтверждения данных
    update_state(callback.from_user.id, STATE_CALLBACK_RENAME_CITY)

    global cityTrue
    global data_called
    global agreeaccaunt
    if callback.data == '🖌Редактировать город':
        data_called = False
        usercitizenRF = f'Выбрано: 🟢{city}'        
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(f'❌Удалить "{city}"', callback_data=f'❌Удалить "{city}"', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('✅Продолжить', callback_data='✅Продолжить', one_time_keyboard=True)
        markup.row(btn2)  
        markup.row(btn3)  
        bot.edit_message_text(usercitizenRF, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif callback.data == '✅Подтвердить':
        data_called = False
        cityTrue = 'True'
        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET  cityAgree = '%s' WHERE id = '%s'" % (cityTrue, id_nubmer_list))
        conn.commit() 
        cur.close()
        conn.close()
        print('сити тру ',cityTrue)
        bot.edit_message_text('✅Данные успешно обновлены!', callback.message.chat.id, callback.message.message_id)
        data(callback.message)

@bot.callback_query_handler(func=lambda callback: callback.data == f'❌Удалить "{city}"')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Продолжить') 
def callback_delete_city(callback):
    # Устанавливаем состояние для удаления или продолжения с городом
    update_state(callback.from_user.id, STATE_CALLBACK_DELETE_CITY)

    if callback.data == f'❌Удалить "{city}"':
        markup = types.InlineKeyboardMarkup()
        btn3 = types.InlineKeyboardButton('✅Добавить город', callback_data='✅Добавить город', one_time_keyboard=True) 
        markup.row(btn3)  
        bot.edit_message_text('Укажи город, где хочешь работать.', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Добавить город') 
def callback_add_city(callback):
    # Устанавливаем состояние для добавления города
    update_state(callback.from_user.id, STATE_CALLBACK_ADD_CITY)

    if callback.data == '✅Добавить город':
        locationCityCitizen(callback.message)        
    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)

def locationCityCitizen(message):
    # Устанавливаем состояние для получения города по геолокации
    update_state(message.from_user.id, STATE_LOCATION_CITY_CITIZEN)

    try:
        global geolocator
        keyboard = types.ReplyKeyboardMarkup()
        button_geo = types.KeyboardButton(text=geolocationButtonText, request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, '⚠️Включи геолокацию на телефоне!⚠️\n\nОтправь свой город👇👇👇\n\nℹ️ Определение города может занять некоторое время🕰.', reply_markup=keyboard)  
        bot.register_next_step_handler(message, location)
        geolocator = Nominatim(user_agent = geolocationNameApp)    
    except Exception:        
        bot.send_message(message.chat.id, phoneError, parse_mode='html')
        bot.register_next_step_handler(message, locationCityCitizen)  
def city_check(coord):
    # Функция не требует установки состояния, так как используется только для проверки города
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
    # Устанавливаем состояние для получения местоположения
    update_state(message.from_user.id, STATE_LOCATION)

    if message.location is not None:           
        a = [message.location.latitude, message.location.longitude]         
        city_name = city_check(a)
        locationcity = city_name
        bot.send_message(message.chat.id, f'{foundedCity} {locationcity}', reply_markup=types.ReplyKeyboardRemove())
        markup = types.InlineKeyboardMarkup()
        btn3 = types.InlineKeyboardButton('✅Продолжить', callback_data='✅Продолжить2', one_time_keyboard=True) 
        markup.row(btn3)  
        bot.send_message(message.chat.id, f'На данный момент нельзя изменить город. Такая возможность будет через 13 дней.\nВыбрано: 🟢{city}', reply_markup=markup)            
    else:        
        bot.send_message(message.chat.id, geolocationError, parse_mode='html')
        bot.register_next_step_handler(message, location)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Продолжить2') 
def callback_message_citizen(callback):
    # Устанавливаем состояние для обработки продолжения в случае завершения редактирования данных
    update_state(callback.from_user.id, STATE_CALLBACK_CONTINUE2_CITIZEN)

    if callback.data == '✅Продолжить2':
        bot.answer_callback_query(callback_query_id=callback.id, text='Сначала нужно завершить редактирование данных. Чтобы завершить нажмите ✅Подтвердить', show_alert=True)
        data(callback.message)
    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)


def handle_state(user_id, message):
    state = get_state(user_id)

    if state == STATE_INPUT_PHONE_NUMBER:
        numberPhoneInput(message)
    elif state == STATE_LOCATION:
        location(message)
    elif state == STATE_INPUT_LASTNAME:
        input_lastname(message)
    elif state == STATE_INPUT_FIRSTNAME: 
        input_firstname(message)
    elif state == STATE_INPUT_MIDDLENAME:
        input_middlename(message)
    elif state == STATE_INPUT_BIRTHDAY:
        input_birtgday(message)
    elif state == STATE_INPUT_BIRTHDAY2:
        input_birtgday2(message)
    elif state == STATE_USER_BIRTHDAY_CHECK:
        user_birthday_check(message)
    elif state == STATE_USER_BIRTHDAY_CHECK2:
        user_birthday_check2(message)
    elif state == STATE_INPUT_PASSPORT:
        input_passport(message)
    elif state == STATE_PASSPORT_CHECK:
        passport_check(message)
    elif state == STATE_READY_PASSPORT_INFO:
        readyPassportInfo(message)
    elif state == STATE_LOCATION_CITY_CITIZEN:
        locationCityCitizen(message)
    elif state == STATE_DATA:
        data(message)
    elif state == STATE_ORDERS:
        orders(message)
    elif state == STATE_CALLBACK_DATA_OF_DATA:
        callback_data_of_data(message)
    elif state == STATE_CALLBACK_INDIVIDUAL:
        callback_individual(message)
    elif state == STATE_INPUT_MY_NALOG_ACCOUNT:
        input_my_nalog_accaunt(message)
    elif state == STATE_MY_NALOG_ACCOUNT_CHECK:
        my_nalog_accaunt_check(message)
    elif state == STATE_CALLBACK_BANK:
        callback_bank(message)
    elif state == STATE_CALLBACK_BANK_CHOICE:
        callback_bank(message)
    elif state == STATE_CALLBACK_CONTINUE2_CITIZEN:
        callback_message_citizen
    elif state == STATE_CALLBACK_CONTINUE:
        callback_edit_data_person(message)
    elif state == STATE_CALLBACK_EDIT_PERSON_DATA:
        callback_edit_person_data_alone(message)
    elif state == STATE_INPUT_LASTNAME2:
        input_lastname2(message)
    elif state == STATE_LASTNAME_CHECK2:
        lastneme_check2(message)
    elif state == STATE_INPUT_FIRSTNAME2:
        input_firstname2(message)
    elif state == STATE_FIRSTNAME_CHECK2:
        firstname_check2(message)
    elif state == STATE_INPUT_MIDDLENAME2:
        input_middlename2(message)
    elif state == STATE_MIDDLENAME_CHECK2:
        middlename_check2(message)
    elif state == STATE_CALLBACK_EDU1:
        callback_data_of_data(message)
    elif state == STATE_CANCEL_CONFIRMATION:
        callback_delete_previos_message(message)
    elif state == STATE_CALLBACK_RENAME_CITY:
        callback_rename_city(message)
    elif state == STATE_CALLBACK_DELETE_CITY:
        callback_delete_city(message)
    elif state == STATE_CALLBACK_ADD_CITY:
        callback_add_city(message)
    else:
        bot.send_message(message.chat.id, "Неизвестное состояние. Попробуйте снова.")

        
if __name__ == '__main__':
    print('Bot started')
    bot.polling(non_stop=True, interval=0, timeout=60, long_polling_timeout=30)