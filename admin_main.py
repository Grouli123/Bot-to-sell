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
# from get_orders_mainArzamas import testMethod
import sendMessageWorker

botApiKey = API_key_one.botAPI

arzamasBot = API_key_Test.botAPIArz
MoskowBot = API_key_Test.botAPIMos
SPBBot = API_key_Test.botAPISan
EkaBot = API_key_Test.botAPIEka

mainApi = None

bot_to_send = None
bot1 = telebot.TeleBot(botApiKey)
bot2 = None

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
workTime = None

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

current_user_id = None

# Состояния для каждого метода
STATE_START = 'start'
STATE_ADMIN_CHECK = 'admin_check'
STATE_INPUT_PASSWORD = 'input_password'
STATE_CITY_OF_OBJ = 'city_of_obj'
STATE_PEOPLE_NEED_COUNT = 'people_need_count'
STATE_INPUT_ADRESS = 'input_adress'
STATE_INPUT_WHATTODO = 'input_whattodo'
STATE_INPUT_STARTWORK = 'input_startwork'
STATE_INPUT_SALARY = 'input_salary'
STATE_INPUT_WORK_TIME = 'input_work_time'
STATE_CREATED_ORDER = 'created_order'

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

def start(message):    
    update_state(message.from_user.id, STATE_START)
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
    global current_user_id
    current_user_id = message.from_user.id
    init_db()
    current_state = get_state(current_user_id)

    global adminChatId
    adminChatId = message.chat.id  
    print(loginin)
    if loginin == False:
        update_state(message.from_user.id, STATE_ADMIN_CHECK)
        bot1.send_message(message.chat.id, 'Введите логин', parse_mode='html')
        bot1.register_next_step_handler(message, admin_check)   
    else:
        start(message)

def check_user_credentials(user_id):
    """Извлекает логин, пароль и статус подписки пользователя из базы данных."""
    conn = sqlite3.connect('custumers.sql')  # Путь к вашей базе данных
    cursor = conn.cursor()
    cursor.execute("SELECT login, password, podpiska FROM custumers WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data if user_data else (None, None, None)

def admin_check(message):
    global loginin, login, password
    global subscription_status
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_admin(message) 
    else:
        user_login, user_password, subscription_status = check_user_credentials(message.from_user.id)
        if user_login is None:
            bot1.send_message(message.chat.id, 'Аккаунт не найден.')
            input_admin(message)
        else:
            login = user_login
            password = user_password
            if login == message.text.strip():
                update_state(message.from_user.id, STATE_INPUT_PASSWORD)
                input_password(message, subscription_status)  
            else:
                bot1.send_message(message.chat.id, 'Логин не найден')
                input_admin(message)

def input_password(message, subscription_status):
    bot1.send_message(message.chat.id, 'Введите пароль', parse_mode='html')
    bot1.register_next_step_handler(message, password_check, subscription_status)

def password_check(message, subscription_status):
    global loginin
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_password(message, subscription_status) 
    else:
        if len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, adressError)
            input_password(message, subscription_status)
        else:
            if password == message.text.strip():
                if subscription_status == 'true':
                    loginin = True
                    start(message)
                else:
                    bot1.send_message(message.chat.id, 'Оплатите подписку, чтобы продолжить')
            else:
                bot1.send_message(message.from_user.id, 'Пароль не подходит')
                input_password(message, subscription_status)

def check_subscription_status(user_id):
    """Проверяет статус подписки пользователя."""
    conn = sqlite3.connect('custumers.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT podpiska FROM custumers WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def city_of_obj(message):
    update_state(message.from_user.id, STATE_CITY_OF_OBJ)
    if loginin:
        if message.text is None:
            bot1.send_message(message.from_user.id, textOnly)
            start(message)
        else:
            if message.text == makeOrderButton:
                subscription_status = check_subscription_status(message.from_user.id)
                if subscription_status == 'true':
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    markup.add('Арзамас', 'Москва и область', 'Екатеринбург', 'Санкт-Петербург')
                    bot1.send_message(message.chat.id, inputCityObject, reply_markup=markup)
                    bot1.register_next_step_handler(message, city_of_obj_check)
                else:
                    bot1.send_message(message.chat.id, 'Оплатите подписку, чтобы продолжить создание заказа')
                    start(message)
            else:
                bot1.send_message(message.chat.id, chooseTruePointOfMenu)
                start(message)
    else:
        bot1.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def city_of_obj_check(message):
    global cityname
    valid_cities = ['Арзамас', 'Москва и область', 'Екатеринбург', 'Санкт-Петербург']
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        city_of_obj(message)
    else:
        city_input = message.text.strip()
        if city_input in valid_cities:
            cityname = city_input
            print(cityname)
            people_need_count(message)
        else:
            bot1.send_message(message.chat.id, 'К сожалению, мы пока не работаем в этом городе')
            city_of_obj(message)

def people_need_count(message):
    update_state(message.from_user.id, STATE_PEOPLE_NEED_COUNT)
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
    update_state(message.from_user.id, STATE_INPUT_ADRESS)
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
    update_state(message.from_user.id, STATE_INPUT_WHATTODO)
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
    update_state(message.from_user.id, STATE_INPUT_STARTWORK)
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
    update_state(message.from_user.id, STATE_INPUT_SALARY)
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
                input_wokr_time(message)
            except ValueError:
                bot1.send_message(message.from_user.id, inputNumbers)
                input_salary(message)

def input_wokr_time(message):
    update_state(message.from_user.id, STATE_INPUT_WORK_TIME)
    bot1.send_message(message.chat.id, "Введите сколько времени потребуется на выполнение работы", parse_mode='html')
    bot1.register_next_step_handler(message, wokr_time_check)

def wokr_time_check(message):      
    global workTime
    if message.text is None:
        bot1.send_message(message.from_user.id, textOnly)
        input_wokr_time(message)
    else:
        if not message.text.strip().isdigit():
            bot1.send_message(message.from_user.id, "Пожалуйста, введите только числовое значение.")
            input_wokr_time(message)
        elif len(message.text.strip()) > maxSymbol1:
            bot1.send_message(message.chat.id, startWorkError)
            input_wokr_time(message) 
        else:     
            try:
                workTime = message.text.strip()                
                int(workTime)
                print("WorkTime =" + workTime)
                created_order(message)
            except ValueError:
                bot1.send_message(message.from_user.id, inputNumbers)
                input_wokr_time(message)


def created_order(message):
    update_state(message.from_user.id, STATE_CREATED_ORDER)
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
    btn2 = types.InlineKeyboardButton(orderSendText, callback_data=orderSendTextCallbackData)
    btn3 = types.InlineKeyboardButton(orderDeleteText, callback_data=orderDeleteCallbackData)
    markup.row(btn2, btn3)    
    sent_message = bot1.send_message(message.chat.id, f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> в {timetostart}:00\n<b>·Рабочее время:</b> {workTime}:00\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>', parse_mode='html', reply_markup=markup)  
    sent_message_id = sent_message.message_id

@bot1.callback_query_handler(func=lambda callback: callback.data == orderSendTextCallbackData)
@bot1.callback_query_handler(func=lambda callback: callback.data == orderDeleteCallbackData)
def callback_message_created_order(callback):
    global feedback
    global chatcity
    global bot2
    if callback.data == orderSendTextCallbackData:
        feedback = orderSendText
        application = f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> в {timetostart}:00\n<b>·Рабочее время:</b> {workTime}:00\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>'
        markup1 = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
        markup1.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, reply_markup=markup1, parse_mode='html')

        # Выбор бота в зависимости от города
        if cityname == 'Арзамас':
            chatcity = arzCity
            bot2 = telebot.TeleBot(arzamasBot)
        elif cityname == 'Екатеринбург':
            chatcity = ekaCity
            bot2 = telebot.TeleBot(EkaBot)
        elif cityname == 'Санкт-Петербург':
            chatcity = sanCity
            bot2 = telebot.TeleBot(SPBBot)
        elif cityname == 'Москва и область':
            chatcity = mosCity
            bot2 = telebot.TeleBot(MoskowBot)

        # Отладочная информация
        print(f"cityname: {cityname}")
        print(f"chatcity: {chatcity}")

        try:
            bot2.send_message(chatcity, application, parse_mode='html', reply_markup=markup1)
        except Exception as e:
            print(f"Error sending message: {e}")

    else:
        feedback = orderDeleteText
        bot1.delete_message(callback.message.chat.id, callback.message.message_id)
    import_into_database(callback.message)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'close_order')
def callback_message_created_order(callback):
    if callback.data == 'close_order':
        conn = sqlite3.connect('applicationbase.sql')
        cursor = conn.cursor()
        message_id = callback.message.message_id
        sql_query = "UPDATE orders SET actualMess = ? WHERE adminMessageId = ?"
        cursor.execute(sql_query, ('False', message_id))
        cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, workTime FROM orders WHERE adminMessageId = ?", (message_id,))
        test2 = cursor.fetchone()
        conn.commit()
        conn.close()
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>Рабочее время:</b> {test2[6]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>'
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
        print("все произошло")
        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()
        cur.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, orderMessageId, orderChatId, workTime FROM orders WHERE adminMessageId = ?", (message_id,))
        users = cur.fetchone()
        # order_info_close = f'❌ Заявка закрыта\n<b>•{users[0]}: </b>{needText} {users[1]} {humanCount}\n<b>•Адрес:</b>👉 {users[2]}\n<b>•Что делать:</b> {users[3]}\n<b>•Начало работ:</:b> в {users[4]}\n<b>Рабочее время:</b>{users[8]}\n<b>•Вам на руки:</:b> <u>{users[5]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        order_info_close = f'❌ Заявка закрыта\n<b>•{users[0]}: </b>{needText} {users[1]} {humanCount}\n<b>•Адрес:</b>👉 {users[2]}\n<b>•Что делать:</b> {users[3]}\n<b>•Начало работ:</b> в {users[4]}\n<b>Рабочее время:</b>{users[8]}\n<b>•Вам на руки:</b> <u>{users[5]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

        user_message_ids = users[6]
        chat_id_list = users[7].split(',') if users[7] else []
        print(f'user_message_ids {user_message_ids}')
        print(f'users[7] {users[7]}')
        message_id_list = user_message_ids.split(',') if user_message_ids else []
        conn.close()
        for chat_id, message_id in zip(chat_id_list, message_id_list):
            print('Чат id: ', chat_id)
            print('Месседж id: ', message_id)
            bot2.edit_message_text(order_info_close, chat_id, message_id, parse_mode='html')

def update_message_with_users_list_test(test):
    global take_user_id
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
            btn02 = types.InlineKeyboardButton('Свернуть', callback_data='collapse_1', one_time_keyboard=True)
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

            btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
            btn02 = types.InlineKeyboardButton('Свернуть', callback_data='collapse', one_time_keyboard=True)
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

@bot1.callback_query_handler(func=lambda callback: callback.data == 'collapse_1')
def testmess_close_one(callback):
    markup = types.InlineKeyboardMarkup()
    btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record_1', one_time_keyboard=True)
    markup.row(btn02)
    bot1.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'collapse')
def testmess_close(callback):
    markup = types.InlineKeyboardMarkup()
    btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
    btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
    markup.row(btn02)
    markup.row(btn01)
    bot1.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'view_record_1')
def testmess_sendAdOne(callback):
    test = callback.message.message_id
    update_message_with_users_list_test(test)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'view_record')
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
        btn01 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='stats_orders', one_time_keyboard=True)
        btn02 = types.InlineKeyboardButton('Назад', callback_data='back', one_time_keyboard=True)
        btn03 = types.InlineKeyboardButton('Отменить заказ', callback_data='cancel_order', one_time_keyboard=True)
        btn04 = types.InlineKeyboardButton('Подтвердить выполнение заказа', callback_data='confirm_order', one_time_keyboard=True)
        btn05 = types.InlineKeyboardButton('Заказ выполнен с браком', callback_data='order_with_defect', one_time_keyboard=True)
        markup.row(btn01)
        if takeParam2[15] != '':
            markup.row(btn04)
            markup.row(btn05)
            markup.row(btn03)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
        print("все произошло")

@bot1.callback_query_handler(func=lambda callback: callback.data == 'back')
def testmess_test(callback):
    message_id = callback.message.message_id
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess, workTime FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()
    if test2[6] == 'True':
        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record_1', one_time_keyboard=True)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'back_1')
def testmess_test_test(callback):
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
        application = f'📞 Телефон: +{takeParam2[2]}\n👤 ФИО: {takeParam2[4]} {takeParam2[5]} {takeParam2[6]}\n📅 Дата рождения: {takeParam2[7]}\n🇷🇺 Гражданство РФ: {takeParam2[8]}\n🤝 Самозанятый: {takeParam2[10]} \n🏙 Город(а): {takeParam2[3]}' 
        markup = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('📊 Статистика заказов', callback_data='stats_orders', one_time_keyboard=True)
        btn02 = types.InlineKeyboardButton('Назад', callback_data='back', one_time_keyboard=True)
        btn03 = types.InlineKeyboardButton('Отменить заказ', callback_data='cancel_order', one_time_keyboard=True)
        btn04 = types.InlineKeyboardButton('Подтвердить выполнение заказа', callback_data='confirm_order', one_time_keyboard=True)
        btn05 = types.InlineKeyboardButton('Заказ выполнен с браком', callback_data='order_with_defect', one_time_keyboard=True)
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

@bot1.callback_query_handler(func=lambda callback: callback.data == 'confirm_order') 
def callback_data_of_data_confirm(callback): 
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
    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess, workTime FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()
    bot1.answer_callback_query(callback.id, "Подтверждение заказа выполнено")
    if test2[6] == 'True':
        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</b> в {test2[4]}\n<b>·Рабочее время:</b>{test2[6]}\n<b>·Вам на руки:</b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</:b>👉 {test2[2]}\n<b>·Что делать:</:b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[6]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record_1', one_time_keyboard=True)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'order_with_defect') 
def callback_data_of_data_miss(callback): 
    conn2 = sqlite3.connect('peoplebase.sql')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT actualOrder, orderMiss FROM users WHERE id = ('%s')" % (take_user_id))
    takeOrderTake = cursor2.fetchone()
    test_test = takeOrderTake[0]
    current_orderId = takeOrderTake[1] if current_orderId else ""
    new_orderId = current_orderId + "," + test_test if current_orderId else test_test
    print(new_orderId, 'ТУТ АЛЕ')
    cursor2.execute("UPDATE users SET actualOrder = '%s', orderMiss = '%s' WHERE id = '%s'" % ("",  new_orderId, take_user_id))
    conn2.commit()
    message_id = callback.message.message_id
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess, workTime FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()
    bot1.answer_callback_query(callback.id, "Заказ был выполнен с браком")
    if test2[6] == 'True':
        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</:b>👉 {test2[2]}\n<b>·Что делать:</:b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</:b>👉 {test2[2]}\n<b>·Что делать:</:b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record_1', one_time_keyboard=True)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'cancel_order') 
def callback_data_of_data_close(callback): 
    message_id = callback.message.message_id
    conn_applicationbase = sqlite3.connect('applicationbase.sql')
    cur_applicationbase = conn_applicationbase.cursor()
    user_name_to_remove = callback.from_user.first_name 
    cur_applicationbase.execute("SELECT adminChatId, adminMessageId, whoTakeId FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    order_info = cur_applicationbase.fetchone()
    if order_info:
        admin_chat_id, admin_message_id, who_take_ids_str = order_info
        who_take_ids = who_take_ids_str.split(',') if who_take_ids_str else []
        if user_name_to_remove in who_take_ids:
            who_take_ids.remove(user_name_to_remove)
        print('Я не знаю', who_take_ids)
        cur_applicationbase.execute("UPDATE orders SET whoTakeId = ('%s') WHERE adminMessageId = ('%s')" % (user_name_to_remove, admin_message_id))
        conn_applicationbase.commit()
    conn_applicationbase.close()
    conn = sqlite3.connect('applicationbase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT cityOfobj, countpeople, adress, whattodo, timetostart, salary, actualMess, workTime FROM orders WHERE adminMessageId = ('%s')" % (message_id))
    test2 = cursor.fetchone()
    bot1.answer_callback_query(callback.id, "Заказ отменен")
    if test2[6] == 'True':
        conn.close()
        application = f'✅\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record', one_time_keyboard=True)
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='close_order', one_time_keyboard=True)
        markup.row(btn02)
        markup.row(btn01)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)
    else:
        application = f'❌ Заявка закрыта\n<b>·{test2[0]}: </b>{needText} {test2[1]} {humanCount}\n<b>·Адрес:</b>👉 {test2[2]}\n<b>·Что делать:</b> {test2[3]}\n<b>·Начало работ:</:b> в {test2[4]}\n<b>·Рабочее время:</:b>{test2[7]}\n<b>·Вам на руки:</:b> <u>{test2[5]}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Посмотреть запись', callback_data='view_record_1', one_time_keyboard=True)
        markup.row(btn02)
        bot1.edit_message_text(application, callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

@bot1.callback_query_handler(func=lambda callback: callback.data == 'stats_orders') 
def callback_data_of_data(callback): 
    global cityTrue
    global isOpenEdit
    global data_called
    global samozanYorN
    global percent_completed
    global percent_failed
    if callback.data == 'stats_orders':  
        data_called = False         
        conn = sqlite3.connect('peoplebase.sql')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = '%s'" % (take_user_id))
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
            percent_completed = (orderCountDone / (orderCountTake)) * 100
            percent_failed = (orderCountMiss / (orderCountTake)) * 100
        except Exception:
            percent_completed = 0
            percent_failed = 0
            print('на ноль делить нельзя')
        markup = types.InlineKeyboardMarkup()
        btn02 = types.InlineKeyboardButton('Назад', callback_data='back_1', one_time_keyboard=True)
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
    global cityname
    global mainApi
    conn = sqlite3.connect('applicationbase.sql')
    cur = conn.cursor()
    cur.execute(insertIntoBase1 % (cityname, countPeople, adress, whattodo, timetostart, orderTime, salary, adminChatId, sent_message_id, '', 'True', '', '', '', '', workTime, '')) 
    conn.commit()
    cur.close()
    conn.close()    
    bot1.send_message(message.chat.id, 'Заявка отправлена')
    state = 'citizenRU'
    print(f'sent_message_id: {sent_message_id}')

    if cityname == 'Арзамас':
        chatcity = arzCity
        # mainApi = arzamasBot

        sendMessageWorker.testMethod(arzamasBot)

        bot2 = telebot.TeleBot(arzamasBot)
    elif cityname == 'Екатеринбург':
        chatcity = ekaCity
        # mainApi = EkaBot
        
        sendMessageWorker.testMethod(EkaBot)

        bot2 = telebot.TeleBot(EkaBot)
    elif cityname == 'Санкт-Петербург':
        chatcity = sanCity
        # mainApi = SPBBot

        sendMessageWorker.testMethod(SPBBot)


        bot2 = telebot.TeleBot(SPBBot)
    elif cityname == 'Москва и область':
        chatcity = mosCity
        # mainApi = MoskowBot

        sendMessageWorker.testMethod(MoskowBot)


        bot2 = telebot.TeleBot(MoskowBot)
    
    print(f"cityname: {cityname}")
    print(f"chatcity: {chatcity}")

    # sendMessageWorker.testMethod(mainApi)
    start(message)

print('Bot started')

bot1.polling(non_stop=True, interval=0, timeout=60, long_polling_timeout=30)