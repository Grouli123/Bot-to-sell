import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime
import registration_people_config.registration_API_key as API_key
import registration_people_config.registration_sqlBase as sqlBase
import registration_people_config.registration_config_message as config_message
import registration_people_config.custumers_sqlBase as sqlBaseCustomer
import citys.city_list as citys
from SendMessIntoAdmin import SendMessageintoHere
from threading import Lock

botApiKey = API_key.botAPI
bot = telebot.TeleBot(botApiKey)

base = sqlBase.createDatabase
insertIntoBase = sqlBase.insertIntoDatabase
nameOfBase = sqlBase.name_of_base

insertIntoAdminOrderBase = sqlBaseCustomer.insertIntoDatabase

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

state = None

user_id = None

registered = False

arzCity = citys.arzamas
ekaCity = citys.ekaterenburg
sanCity = citys.sankt_peterburg
mosCity = citys.moskow

adminchatcity = 'AdGraeBot'

chatcity = None

cityTrue = 'False'

actualOrder = ''
orderTake = ''
orderDone = ''
orderMiss = ''
raiting = ''
orderDefect = ''

user_id_order = None
phoneOrder = None
lastnameOrder = None
firstnameOrder = None
middlenameOrder = None
loginOrder = None
passwordOrder = None
cityOrder = None

baseCustomer = sqlBaseCustomer.createDatabase

nameOfBaseCustomer = sqlBaseCustomer.name_of_base

customerBaseName = 'custumers.sql'
workersBaseName = 'peoplebase.sql'

current_user_id  = None

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

@bot.message_handler(commands=['start'])
def registration(message):
    # global user_id    
    global current_user_id
    current_user_id = message.from_user.id
    print(f'Start - ваш ID: {current_user_id}')  # Отладка
    init_db()
    current_state = get_state(current_user_id)
    
    if current_state is None:  # Если состояние не установлено
        update_state(current_user_id, 'registration')
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('Я заказчик', callback_data='Заказчик', one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton('Я рабочий', callback_data='Рабочий', one_time_keyboard=True)
        markup.row(btn2, btn3)
        bot.send_message(message.chat.id, f'Выберите пункт:', parse_mode='html', reply_markup=markup)
    else: 
        handle_state(current_user_id, message)
   

def numberPhoneInput(message, user_id=None):
    if user_id is None:
        user_id = current_user_id  # Используем сохраненный user_id, если не передан
    
    print(f'numberPhoneInput - ваш ID: {user_id}')  # Отладка

    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    cur.execute(base)
    conn.commit()
    
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cur.fetchone()
    
    if existing_user is None:
        # Если пользователь не найден, добавляем его в базу данных
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        update_state(user_id, 'numberPhoneInput')
        
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
        keyboard.add(button_phone)
        
        bot.send_message(message.chat.id, phoneMessageText, reply_markup=keyboard, parse_mode='html')
        bot.register_next_step_handler(message, lambda msg: geolocation(msg, user_id))
    else:
        cur.execute("SELECT botchatname, city FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        chatcity = result[0]
        locationcity = result[1]
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBase, url=f'https://t.me/{chatcity}'))
        
        bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    
    cur.close()
    conn.close()


def geolocation(message, user_id=None):
    global phone
    if user_id is None:
        user_id = current_user_id # Используем user_id из сообщения, если не передан
    
    try:
        phone = message.contact.phone_number
        if phone.startswith('+7') or phone.startswith('7'):
            global geolocator
            update_state(user_id, 'geolocation')
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text=geolocationButtonText, request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.chat.id, geolocationMessageText, reply_markup=keyboard)
            bot.register_next_step_handler(message, lambda msg: location(msg))
            geolocator = Nominatim(user_agent = geolocationNameApp)  
            
            insert_user_data(workersBaseName, 'phone', phone, user_id)  
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, f"Недопустимый номер {phone}.\n\nПривет!\n\nДавай пройдём короткую регистрацию🤝Для начала - поделись номером телефона!👇👇👇👇👇", reply_markup=keyboard, parse_mode='html')
            bot.register_next_step_handler(message, lambda msg: geolocation(msg, user_id))   
    except Exception:        
        bot.send_message(message.chat.id, phoneError, parse_mode='html')
        bot.register_next_step_handler(message, lambda msg: geolocation(msg, user_id))


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
    user_id = message.from_user.id  # Получаем user_id из сообщения
    
    if message.location is not None:           
        a = [message.location.latitude, message.location.longitude]         
        city_name = city_check(a)
        locationcity = city_name
        print(f"Записываем {locationcity} для user_id {user_id}")  # Отладочная информация
        insert_user_data(workersBaseName, 'city', locationcity, user_id)
        bot.send_message(message.chat.id, f'{foundedCity} {locationcity}', reply_markup=types.ReplyKeyboardRemove())
        input_lastname(message)   
    else:        
        bot.send_message(message.chat.id, geolocationError, parse_mode='html')
        bot.register_next_step_handler(message, location)

        
def input_lastname(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_lastname')
    bot.send_message(message.chat.id, lastnameText, parse_mode='html')
    bot.register_next_step_handler(message, lastneme_check)   

def lastneme_check(message):
    global lastname
    user_id = message.from_user.id 
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
            
            insert_user_data(workersBaseName, 'last_name', lastname, user_id)  
            input_firstname(message)


def input_firstname(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_firstname')
    bot.send_message(message.chat.id, firstnameText, parse_mode='html')
    bot.register_next_step_handler(message, firstname_check)

def firstname_check(message):       
    global firstname
    user_id = message.from_user.id 
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
            
            insert_user_data(workersBaseName, 'firts_name', firstname, user_id) 
            input_middlename(message)
        
def input_middlename(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_middlename')
    bot.send_message(message.chat.id, middlenameText, parse_mode='html')
    bot.register_next_step_handler(message, middlename_check)

def middlename_check(message):      
    global middlename
    user_id = message.from_user.id 
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
            insert_user_data(workersBaseName, 'middle_name', middlename, user_id) 
            input_birtgday(message)

def numberPhoneInput_order(message):
    # conn = sqlite3.connect('custumers.sql')
    # cur = conn.cursor()
    # cur.execute(baseCustomer)
    # conn.commit()
    # cur.execute("SELECT * FROM custumers WHERE user_id = ?", (user_id,))
    # existing_user = cur.fetchone()
    
    update_state(user_id, 'numberPhoneInput_order')
    # if existing_user is None:
        # Если пользователь не найден, добавляем его в базу данных
        # cur.execute("INSERT INTO custumers (user_id) VALUES (?)", (user_id,))
        # conn.commit()
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, phoneMessageText, reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, number_check)
    # else:
    #     cur.execute("SELECT botchatname, city FROM custumers WHERE user_id = ?", (user_id,))
    #     result = cur.fetchone()
    #     chatcity = result[0]
    #     locationcity = result[1]
    #     markup = types.InlineKeyboardMarkup()
    #     markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBaseCustomer, url=f'https://t.me/{chatcity}'))
    #     bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    # cur.close()
    # conn.close()

def number_check(message):    
    global phoneOrder 
    try:
        phoneOrder = message.contact.phone_number
        if phoneOrder.startswith('+7') or phoneOrder.startswith('7'):
            bot.send_message(message.chat.id, f'Отлично, осталось немного', reply_markup=types.ReplyKeyboardRemove()) 
            input_lastname_order(message)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text=phoneButtonText, request_contact=True)
            keyboard.add(button_phone)
            bot.send_message(message.chat.id, f"Недопустимый номер {phoneOrder}.\n\nПривет!\n\nДавай пройдём короткую регистрацию🤝Для начала - поделись номером телефона!👇👇👇👇👇", reply_markup=keyboard, parse_mode='html')
            bot.register_next_step_handler(message, number_check)   
    except Exception:        
        bot.send_message(message.chat.id, phoneError, parse_mode='html')
        bot.register_next_step_handler(message, number_check)   

def input_lastname_order(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_lastname_order')
    bot.send_message(message.chat.id, lastnameText, parse_mode='html')
    bot.register_next_step_handler(message, lastneme_check_order)   

def lastneme_check_order(message):
    global lastnameOrder 
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_lastname_order(message) 
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, lastnameError)
            message.text.strip(None)
            input_lastname_order(message) 
        else:
            lastnameOrder = message.text.strip()
            input_firstname_order(message)

def input_firstname_order(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_firstname_order')
    bot.send_message(message.chat.id, firstnameText, parse_mode='html')
    bot.register_next_step_handler(message, firstname_check_order)

def firstname_check_order(message):       
    global firstnameOrder 
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_firstname_order(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_firstname_order(message)        
        else:                  
            firstnameOrder = message.text.strip()   
            input_middlename_order(message)
        
def input_middlename_order(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_middlename_order')
    bot.send_message(message.chat.id, middlenameText, parse_mode='html')
    bot.register_next_step_handler(message, middlename_check_order)

def middlename_check_order(message):      
    global middlenameOrder
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_middlename_order(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, middlenameError)
            message.text.strip(None)
            input_middlename_order(message) 
        else:     
            middlenameOrder = message.text.strip()
            city_order(message)

def city_order(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Москва и МО', callback_data='Москва и МО', one_time_keyboard=True)
    btn2 = types.InlineKeyboardButton('Екатеринбург', callback_data='Екатеринбург', one_time_keyboard=True)
    btn3 = types.InlineKeyboardButton('Санкт-Петербург', callback_data='Санкт-Петербург', one_time_keyboard=True)
    btn4 = types.InlineKeyboardButton('Арзамас', callback_data='Арзамас', one_time_keyboard=True)
    markup.row(btn1, btn2)  
    markup.row(btn3, btn4)   
    bot.send_message(message.chat.id, f'Выберите пункт:', parse_mode='html', reply_markup=markup)  

def input_login_order(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_login_order')
    bot.send_message(message.chat.id, 'Введите ВАШ будущий логин: ', parse_mode='html')
    bot.register_next_step_handler(message, login_check_order)

def login_check_order(message):       
    global loginOrder 
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_login_order(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_login_order(message)        
        else:                  
            loginOrder = message.text.strip()   
            print(loginOrder, ' login')
            input_password_order(message)

def input_password_order(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_password_order')
    bot.send_message(message.chat.id, 'Введите ВАШ будущий пароль: ', parse_mode='html')
    bot.register_next_step_handler(message, password_check_order)

def password_check_order(message):       
    global passwordOrder 
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_password_order(message)
    else:
        if len(message.text.strip()) > maxSymbol:
            bot.send_message(message.chat.id, firstnameError)
            message.text.strip(None)
            input_password_order(message)        
        else:                  
            user_id = message.from_user.id

            passwordOrder = message.text.strip()   
            print(passwordOrder, ' pawwword')
            sendMoney(message, user_id)

def sendMoney(message, user_id):
    print(user_id)
    import_into_database_order_admin(message, user_id)
    markup1 = types.InlineKeyboardMarkup()
    btn01 = types.InlineKeyboardButton('💵 Оплатить', url='https://t.me/Grouli123', one_time_keyboard=True)
    markup1.row(btn01)
    bot.send_message(message.from_user.id, f'Стоимость месячной подписки 5.000 рублей\nОплатить можно переводом по номеру +79965638345 ТОЛЬКО НА (ОЗОН БАНК)\nПо кнопке ниже вы перейдете на нашего менеджера.\nОтправьте ему в чат:\n\n1.ФИО от кого вы отправили перевод\n2.Скриншот перевода\ 3.ФИО зарегистрированного заказчика для активации\n\nПосле поступления денежных средств на счет, ваша подписка будет активирована и вы сможете выставлять заказы\n\nЗа ошибки в номере телефона или банке при совершении оплаты мы ответственности не несем.\nПеревод строго по указанному номеру и на указанный банк!', reply_markup= markup1)

def input_birtgday(message):
    user_id = message.from_user.id
    update_state(user_id, 'input_birtgday')
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
    user_id = message.from_user.id 
    try:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_birtgday(message)
        else:
            userbirthday = get_date(message.text.strip())
            if userbirthday:
                insert_user_data(workersBaseName, 'birthday', userbirthday, user_id) 
                citizenRU(message)
            else:
                bot.send_message(message.chat.id, dateError)
                bot.register_next_step_handler(message, user_birthday_check)
    except ValueError:
        bot.send_message(message.chat.id, dateError)
        bot.register_next_step_handler(message, user_birthday_check)

def citizenRU(message):
    global state
    user_id = message.from_user.id
    update_state(user_id, 'citizenRU')
    state = 'initial'
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
    
    user_id = callback.from_user.id
    if callback.data == citizenRuButtonYesTextCallbackData:
        usercitizenRF = citizenRuButtonYesText        
        bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    else:          
        usercitizenRF = citizenRuButtonNoText
        bot.edit_message_text(userCitizenRuText, callback.message.chat.id, callback.message.message_id)
    registered = True
    insert_user_data(workersBaseName, 'citizenRF', usercitizenRF, user_id)
    bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: {usercitizenRF}\n🏙 Город(а): {locationcity}')
     
    city_check_for_chat(callback.message, user_id)

@bot.callback_query_handler(func=lambda callback: callback.data == 'Заказчик')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Рабочий') 
def callback_message_citizen(callback):   
    global usercitizenRF 
    global registered
    if callback.data == 'Заказчик':
        user_id_test = callback.from_user.id
        print(f"Пользователь с ID {user_id_test} нажал кнопку 'Заказчик'")

        bot.edit_message_text('Выберите пункт: ', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Заказчик')
        numberPhoneInput_order(callback.message)

    elif callback.data == 'Рабочий':  
        bot.edit_message_text('Выберите пункт: ', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Рабочий')
        numberPhoneInput(callback.message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'Москва и МО')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Екатеринбург') 
@bot.callback_query_handler(func=lambda callback: callback.data == 'Санкт-Петербург') 
@bot.callback_query_handler(func=lambda callback: callback.data == 'Арзамас') 
def callback_message_citizen(callback): 
    global cityOrder  
    if callback.data == 'Москва и МО':
        cityOrder = 'Москва и МО'
        bot.edit_message_text('Москва и МО', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Я вас понял: Москва и МО')
        input_login_order(callback.message)

    elif callback.data == 'Екатеринбург':  
        cityOrder = 'Екатеринбург'
        bot.edit_message_text('Екатеринбург', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Я вас понял: Екатеринбург')
        input_login_order(callback.message)

    elif callback.data == 'Санкт-Петербург': 
        cityOrder = 'Санкт-Петербург' 
        bot.edit_message_text('Санкт-Петербург', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Я вас понял: Санкт-Петербург')
        input_login_order(callback.message)
    
    elif callback.data == 'Арзамас':  
        cityOrder = 'Арзамас' 
        bot.edit_message_text('Арзамас', callback.message.chat.id, callback.message.message_id)        
        bot.send_message(callback.message.chat.id, 'Я вас понял: Арзамас')
        input_login_order(callback.message)

# Основная функция для проверки состояния и вызова соответствующего метода
def handle_state(user_id, message):
    state = get_state(user_id)

    if state == 'numberPhoneInput':
        numberPhoneInput(message)
    elif state == 'geolocation':
        geolocation(message)
    elif state == 'input_lastname':
        input_lastname(message)
    elif state == 'input_firstname':
        input_firstname(message)
    elif state == 'input_middlename':
        input_middlename(message)
    elif state == 'numberPhoneInput_order':
        numberPhoneInput_order(message)
    elif state == 'input_lastname_order':
        input_lastname_order(message)
    elif state == 'input_firstname_order':
        input_firstname_order(message)
    elif state == 'input_middlename_order':
        input_middlename_order(message)
    elif state == 'input_login_order':
        input_login_order(message)
    elif state == 'input_password_order':
        input_password_order(message)
    elif state == 'input_birtgday':
        input_birtgday(message)
    elif state == 'citizenRU':
        citizenRU(message)

@bot.message_handler(content_types=['text'])
def check_state(message):
    user_id = message.from_user.id
    handle_state(user_id, message)

@bot.message_handler(content_types=['text'])
def check_callback_message_citizen(message):          
        global state      
        user_id = message.from_user.id
        if state == 'initial':         
            bot.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            citizenRU(message)         
        elif state == 'citizenRU':
            bot.send_message(message.chat.id, registrationSucsess, parse_mode='html')
            city_check_for_chat(message, user_id)

def city_check_for_chat(message, user_id):
    global chatcity
    if locationcity == 'Арзамас':
        chatcity = arzCity        
        import_into_database(message, user_id)
    elif locationcity == 'Екатеринбург':
        chatcity = ekaCity
        import_into_database(message, user_id)
    elif locationcity == 'Санкт-Петербург':
        chatcity = sanCity
        import_into_database(message, user_id)
    elif locationcity == 'Москва':
        chatcity = mosCity
        import_into_database(message, user_id)
    else: 
        bot.send_message(message.chat.id, 'К сожалению, мы не работаем по вашему городу')

def import_into_database(message, user_id):
    global state  
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    # cur.execute(insertIntoBase % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF, user_id, samozanatost, agreeaccaunt, passport, chatcity, cityTrue, actualOrder, orderTake, orderDone, orderMiss, 'None', raiting)) 
    # cur.execute(sqlBase.updateDatabase % (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF, samozanatost, agreeaccaunt, passport, chatcity, cityTrue, actualOrder, orderTake, orderDone, orderMiss, 'None', raiting, user_id))
    cur.execute(sqlBase.updateDatabase, (phone, locationcity, lastname, firstname, middlename, userbirthday, usercitizenRF, samozanatost, agreeaccaunt, passport, chatcity, cityTrue, actualOrder, orderTake, orderDone, orderMiss, 'None', raiting, '', user_id))

    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'{buttonResultName} {locationcity}', callback_data=nameOfBase, url=f'https://t.me/{chatcity}'))
    bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
    state = 'citizenRU'

def import_into_database_order_admin(message, user_id):
    global state
    
    try:
        # First, let's create the database
        conn = sqlite3.connect('custumers.sql')
        cur = conn.cursor()
        
        # Execute the CREATE TABLE statement
        cur.execute(sqlBaseCustomer.createDatabase)
        
        # Commit the changes
        conn.commit()
        
        # Check if the table was created successfully
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='custumers'")
        if cur.fetchone():
            print("Database and table created successfully.")
            
            # Now, let's insert the data
            cur.execute(insertIntoAdminOrderBase % (
                phoneOrder, cityOrder, lastnameOrder, firstnameOrder, 
                middlenameOrder, user_id, loginOrder, passwordOrder, 
                False, chatcity
            ))
            
            # Commit the changes
            conn.commit()
            
            # Close the connection
            cur.close()
            conn.close()
            
            # Send message with inline keyboard
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f'{buttonResultName} для создания заказов', callback_data=nameOfBase, url=f'https://t.me/{adminchatcity}'))
            bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)
            
            state = 'citizenRU'
            print(user_id)
            SendMessageintoHere(6171671445, user_id)
        else:
            print("Failed to create database or table.")
            # Handle the error case (e.g., send an error message to the user)
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        # Handle the error case (e.g., send an error message to the user)
    
    finally:
        # Ensure the connection is closed
        if conn:
            # cur.close()
            conn.close()

# def import_into_database_order_admin(message, user_id):
#     global state  
#     # global user_id
#     conn = sqlite3.connect('custumers.sql')
#     cur = conn.cursor()
#     sqlBaseCustomer.createDatabase
#     cur.execute(insertIntoAdminOrderBase % (phoneOrder, cityOrder, lastnameOrder, firstnameOrder, middlenameOrder, user_id, loginOrder, passwordOrder, False, chatcity)) 
#     conn.commit()
#     cur.close()
#     conn.close()
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton(f'{buttonResultName} для создания заказов', callback_data=nameOfBase, url=f'https://t.me/{adminchatcity}'))       
#     bot.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)    
#     state = 'citizenRU'    
#     print(user_id)
#     SendMessageintoHere(6171671445, user_id)

print('Bot started')

bot.polling(non_stop=True, interval=0, timeout=60, long_polling_timeout=30)
