import telebot
from telebot import types
import sqlite3
import json
import os.path
import admin_config.admin_sqlBase as sqlBase_one
import admin_config.admin_config_message as config_message_one
import get_orders_config.get_orders_config_message as config_message_bot_order
import citys.city_list as citys
from SendMessIntoAdmin import SendMessageintoHere
from get_orders_mainArzamas import sendNotyfiMessage

botApiKey13 = '6433261921:AAEmTi8RVvhuSdYSlxB2uq0x3tP0X4wMRBE'
bot13 = telebot.TeleBot(botApiKey13)

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

# Переменные для отслеживания состояния
STATE_AWAITING_LOGIN = 'awaiting_login'
STATE_AWAITING_PASSWORD = 'awaiting_password'
STATE_LOGGED_IN = 'logged_in'
STATE_OPENED_ORDERS = 'opened_orders'
STATE_OPENED_PEOPLE = 'opened_people'
STATE_OPENED_ADMIN_DB = 'opened_admin_db'
STATE_DISPLAYED_ADMINS = 'displayed_admins'
STATE_INPUTTING_MESSAGE = 'inputting_message'
STATE_MESSAGE_READY_TO_SEND = 'message_ready_to_send'
STATE_SENDING_MESSAGE = 'sending_message'
STATE_CANCEL_MESSAGE = 'cancel_message'

# Создаем соединение с базой данных для хранения состояний пользователей
def init_db():
    conn = sqlite3.connect('states.sql')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_states (
                      user_id INTEGER PRIMARY KEY,
                      state TEXT)''')
    conn.commit()
    conn.close()

init_db()  # Инициализация базы данных при запуске

# Функция для обновления состояния пользователя
def update_state(user_id, state):
    conn = sqlite3.connect('states.sql')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_states (user_id, state) VALUES (?, ?)', (user_id, state))
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

# Функция старта
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn2 = types.InlineKeyboardButton(config_message_one.open_base_orders, callback_data='open_orders')
    btn3 = types.InlineKeyboardButton(config_message_one.open_base_people, callback_data='open_people')
    btn4 = types.InlineKeyboardButton('Открыть базу данных админов', callback_data='open_admin_db')
    btn5 = types.InlineKeyboardButton('Отображение админов', callback_data='display_admins')    
    btn6 = types.InlineKeyboardButton('Ввести сообщение', callback_data='input_message')      
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    markup.add(btn6)
    bot13.send_message(message.chat.id, config_message_one.start_bot_message, reply_markup=markup)

@bot13.message_handler(commands=['start'])
def input_admin(message):      
    global adminChatId
    adminChatId = message.chat.id  
    user_state = get_state(message.chat.id)
    if user_state:
        if user_state == STATE_LOGGED_IN:
            start(message)
        elif user_state == STATE_AWAITING_LOGIN:
            bot13.send_message(message.chat.id, 'Введите логин', parse_mode='html')
            bot13.register_next_step_handler(message, admin_check)
        elif user_state == STATE_AWAITING_PASSWORD:
            bot13.send_message(message.chat.id, 'Введите пароль', parse_mode='html')
            bot13.register_next_step_handler(message, password_check)
    else:
        bot13.send_message(message.chat.id, 'Введите логин', parse_mode='html')
        update_state(message.chat.id, STATE_AWAITING_LOGIN)
        bot13.register_next_step_handler(message, admin_check)

def admin_check(message):
    if message.text is None:
        bot13.send_message(message.from_user.id, config_message_one.message_should_be_text_type)
        input_admin(message) 
    else:
        if len(message.text.strip()) > config_message_one.max_symbol_for_message:
            bot13.send_message(message.chat.id, config_message_one.adress_error)
            input_admin(message) 
        else:
            if 'admin' == message.text.strip():  # Пример логина
                input_password(message)
                update_state(message.chat.id, STATE_AWAITING_PASSWORD)
            else:
                bot13.send_message(message.from_user.id, 'Логин не найден')
                input_admin(message)

def input_password(message):
    bot13.send_message(message.chat.id, 'Введите пароль', parse_mode='html')
    bot13.register_next_step_handler(message, password_check)   

def password_check(message):
    global loginin
    if message.text is None:
        bot13.send_message(message.from_user.id, config_message_one.message_should_be_text_type)
        input_password(message) 
    else:
        if len(message.text.strip()) > config_message_one.max_symbol_for_message:
            bot13.send_message(message.chat.id, config_message_one.adress_error)
            input_password(message) 
        else:
            if 'admin123' == message.text.strip():  # Пример пароля
                loginin = True
                update_state(message.chat.id, STATE_LOGGED_IN)
                start(message)
            else:
                bot13.send_message(message.from_user.id, 'Пароль не подходит')
                input_password(message)

@bot13.callback_query_handler(func=lambda call: call.data == 'open_orders')
def handle_open_base_orders(call):
    update_state(call.message.chat.id, STATE_OPENED_ORDERS)
    bot13.send_message(call.message.chat.id, config_message_one.open_base_orders_message)
    show_database_orders(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'open_people')
def handle_open_base_people(call):
    update_state(call.message.chat.id, STATE_OPENED_PEOPLE)
    bot13.send_message(call.message.chat.id, config_message_one.open_base_people_message)
    show_database_users(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'open_admin_db')
def handle_open_admin_db(call):
    update_state(call.message.chat.id, STATE_OPENED_ADMIN_DB)
    bot13.send_message(call.message.chat.id, 'Открыть базу данных админов')
    show_database_userOrder(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'display_admins')
def display_admins(call):
    update_state(call.message.chat.id, STATE_DISPLAYED_ADMINS)
    send_customers_keyboard(call.message)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'input_message')
def input_message(call):
    update_state(call.message.chat.id, STATE_INPUTTING_MESSAGE)
    bot13.send_message(call.message.chat.id, 'Введите сообщение:', parse_mode='html')
    bot13.register_next_step_handler(call.message, get_message)

def get_message(message):
    user_message_ids[message.chat.id] = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_send = types.InlineKeyboardButton('Отправить', callback_data='send_message')
    btn_cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel_message')
    markup.add(btn_send, btn_cancel)
    bot13.send_message(message.chat.id, f'Ваше сообщение: {message.text}', reply_markup=markup)
    update_state(message.chat.id, STATE_MESSAGE_READY_TO_SEND)

@bot13.callback_query_handler(func=lambda call: call.data == 'send_message')
def send_message(call):
    user_message = user_message_ids.get(call.message.chat.id)
    if user_message:
        bot13.send_message(adminChatId, f'Сообщение от пользователя: {user_message}')
        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
            order_id = cur.fetchone()[0]
            cur.execute("UPDATE orders SET notifyMessageWorkers = ? WHERE id = ?", (user_message, order_id))
            conn.commit()
            sendNotyfiMessage()
            bot13.send_message(call.message.chat.id, 'Сообщение отправлено')
        except sqlite3.Error as e:
            print(f"Ошибка записи в базу данных: {e}")
        finally:
            cur.close()
            conn.close()
        bot13.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        del user_message_ids[call.message.chat.id]
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'cancel_message')
def cancel_message(call):
    bot13.send_message(call.message.chat.id, 'Сообщение отменено')
    if call.message.chat.id in user_message_ids:
        del user_message_ids[call.message.chat.id]
        bot13.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot13.answer_callback_query(call.id)

def send_customers_keyboard(message, page=0):
    conn = sqlite3.connect('custumers.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT last_name, firts_name, middle_name, id, podpiska FROM custumers') 
    customers = cursor.fetchall()
    conn.close()
    per_page = 10
    start = page * per_page
    end = start + per_page
    paginated_customers = customers[start:end]
    keyboard = types.InlineKeyboardMarkup()
    for customer in paginated_customers:
        full_name = ' '.join(customer[:3])
        subscription_status = "Дезактивировать" if customer[4] == 'true' else "Активировать"
        callback_data = f"customer_{customer[3]}_{subscription_status.lower()}"
        keyboard.add(types.InlineKeyboardButton(full_name, callback_data=callback_data))
    if len(customers) > end:
        keyboard.add(types.InlineKeyboardButton("Вперед", callback_data=f"page_{page+1}"))
    if page > 0:
        keyboard.add(types.InlineKeyboardButton("Назад", callback_data=f"page_{page-1}"))
    bot13.send_message(message.chat.id, "Выберите пользователя:", reply_markup=keyboard)

@bot13.callback_query_handler(func=lambda call: call.data.startswith('customer_'))
def toggle_subscription(call):
    parts = call.data.split('_')
    customer_id = parts[1]
    action = parts[2]  
    conn = sqlite3.connect('custumers.sql')
    cur = conn.cursor()
    cur.execute('SELECT last_name, firts_name, middle_name, podpiska FROM custumers WHERE id = ?', (customer_id,))
    customer = cur.fetchone()
    new_status = 'true' if action == "активировать" else 'false'
    cur.execute('UPDATE custumers SET podpiska = ? WHERE id = ?', (new_status, customer_id))
    conn.commit()
    conn.close()
    full_name = ' '.join(customer[:3])
    subscription_status = "Подписка активна" if new_status == 'true' else "Подписка не активна"
    toggle_button_text = "Дезактивировать" if new_status == 'true' else "Активировать"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(toggle_button_text, callback_data=f"customer_{customer_id}_{toggle_button_text.lower()}"))
    bot13.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{full_name}\nСтатус: {subscription_status}", reply_markup=keyboard)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def page_callback(call):
    page = int(call.data.split('_')[1])
    send_customers_keyboard(call.message, page)
    bot13.answer_callback_query(call.id)

@bot13.callback_query_handler(func=lambda call: call.data == 'back_to_list')
def back_to_list(call):
    send_customers_keyboard(call.message)

def show_database_orders(message):
    if loginin:
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
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def show_database_users(message):
    if loginin:
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
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def show_database_userOrder(message):
    if loginin:
        if not os.path.exists('custumers.sql'):
            bot13.send_message(message.chat.id, "База данных пустая")
        else:
            conn = sqlite3.connect('custumers.sql')
            cur = conn.cursor()
            cur.execute('SELECT * FROM custumers')
            users = cur.fetchall()
            info = ''
            for el in users:
                info += f'3:{el[2]} 4:{el[3]} 5:{el[4]} 6:{el[5]} 7:{el[6]} 8:{el[7]} 9:{el[8]} 10:{el[9]}\n\n11:{el[10]}'
            cur.close()
            conn.close()
            bot13.send_message(message.chat.id, info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

@bot13.message_handler(content_types=['text'])
def check_state(message):
    user_id = message.from_user.id
    handle_state(user_id, message)

# Обработчик состояний пользователя
def handle_state(user_id, message):
    state = get_state(user_id)

    if state == STATE_AWAITING_LOGIN:
        input_admin(message)
    elif state == STATE_AWAITING_PASSWORD:
        input_password(message)
    elif state == STATE_LOGGED_IN:
        start(message)
    elif state == STATE_OPENED_ORDERS:
        handle_open_base_orders(message)
    elif state == STATE_OPENED_PEOPLE:
        handle_open_base_people(message)
    elif state == STATE_OPENED_ADMIN_DB:
        handle_open_admin_db(message)
    elif state == STATE_DISPLAYED_ADMINS:
        display_admins(message)
    elif state == STATE_INPUTTING_MESSAGE:
        input_message(message)
    elif state == STATE_MESSAGE_READY_TO_SEND:
        send_message(message)
    elif state == STATE_SENDING_MESSAGE:
        get_message(message)
    elif state == STATE_CANCEL_MESSAGE:
        cancel_message(message)

print('Bot started')
bot13.polling(non_stop=True, interval=0, timeout=60, long_polling_timeout=30)