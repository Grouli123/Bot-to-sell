import telebot
from telebot import types
import sqlite3
import json

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

def start(message):    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn2 = types.KeyboardButton(openBaseOrders)
    btn3 = types.KeyboardButton(openBasePeople)
    btn4 = types.KeyboardButton('Открыть базу данных админов')
    markup.row(btn2, btn3)    
    markup.row(btn4)    
    bot13.send_message(message.chat.id, startBotMessage,  reply_markup=markup)
    bot13.register_next_step_handler(message, city_of_obj)
    send_customers_keyboard(message)


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

def city_of_obj(message):
    if loginin == True:
        if message.text is None:
            bot13.send_message(message.from_user.id, textOnly)
            start(message) 
        else:
            if message.text == openBaseOrders:
                bot13.send_message(message.chat.id, openBseOrdersMessage)
                show_database_orders(message)
                start(message)
            elif message.text == openBasePeople:
                bot13.send_message(message.chat.id, openBasePeopleMessage)
                show_database_users(message)
                start(message)
            elif message.text == 'Открыть базу данных админов':
                bot13.send_message(message.chat.id, 'Открыть базу данных админов')
                show_database_userOrder(message)
                start(message)
            else:
                bot13.send_message(message.chat.id, chooseTruePointOfMenu)            
                start(message)  
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

# def SendMessageintoHere():
#     print('itWork')
    # global check_mess_already_send
    # global check_user_id
    # global last_sent_message

    # global humanCount
    # global needText
    # global last_message_id
    # global error_reported
    # global user_last_message_ids
    # global user_message_ids

    # global user_chat_ids
    # global data_called
    # global user_id_mess
    # data_called = False

    # conn5 = sqlite3.connect('peoplebase.sql')
    # cur5 = conn5.cursor()
    # cur5.execute("SELECT botChatId FROM users")
    
    # results = cur5.fetchall()

    # conn = sqlite3.connect('applicationbase.sql')
    # cur = conn.cursor()

    # try:
    #     cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
    #     users = cur.fetchone() 
        
    #     if users is not None:
    #         if (int(users[3]) <= 1) or (int(users[3]) >= 5):
    #             humanCount = 'человек'
    #         else:
    #             humanCount = 'человека'
                    
    #         if int(users[3]) > 1:
    #             needText = 'Нужно'
    #         else:
    #             needText = 'Нужен'

    #         if (int(users[3]) <= 1):
    #             markup2 = types.InlineKeyboardMarkup()
    #             btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
    #             btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
    #             markup2.row(btn12)  
    #             markup2.row(btn52)            
    #         elif (int(users[3]) == 2):
    #             markup2 = types.InlineKeyboardMarkup()
    #             btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
    #             btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
    #             btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
    #             markup2.row(btn12)  
    #             markup2.row(btn22)  
    #             markup2.row(btn52) 
    #         elif (int(users[3]) == 3):
    #             markup2 = types.InlineKeyboardMarkup()
    #             btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
    #             btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
    #             btn32 = types.InlineKeyboardButton('Едем в 3', callback_data='Едем в 3', one_time_keyboard=True)
    #             btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
    #             markup2.row(btn12)  
    #             markup2.row(btn22)  
    #             markup2.row(btn32)  
    #             markup2.row(btn52) 
    #         elif (int(users[3]) >= 4):
    #             markup2 = types.InlineKeyboardMarkup()
    #             btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
    #             btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
    #             btn32 = types.InlineKeyboardButton('Едем в 3', callback_data='Едем в 3', one_time_keyboard=True)
    #             btn42 = types.InlineKeyboardButton('Едем в 4', callback_data='Едем в 4', one_time_keyboard=True)
    #             btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
    #             markup2.row(btn12)  
    #             markup2.row(btn22)  
    #             markup2.row(btn32)  
    #             markup2.row(btn42)  
    #             markup2.row(btn52)             
                
    #         order_info = f'✅\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n<b>•Адрес:</b>👉 {users[4]}\n<b>•Что делать:</b> {users[5]}\n<b>•Начало работ:</b> в {users[6]}\n<b>•Вам на руки:</b> <u>{users[8]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
                
    #         if order_info != last_sent_message:
                    
    #             print('работает елсе')

    #             # Получаем ID пользователя
    #             user_id_mess = users[0]
    #             print(user_id_mess)
    #             # Получаем текущий список message_id из базы данных
    #             cur.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % (user_id_mess))
    #             current_message_ids_str = cur.fetchone()[0]
                    
    #             # Преобразуем текущую строку в список (если она не пуста)
    #             current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []
                
    #             for result in results:
    #                 botChatIdw = result[0]  # Получаем значение botChatId из результата
    #                 if botChatIdw != 'None':
    #                     print("Заполненное значение botChatId:", botChatIdw)

    #             # messageChatId = message.chat.id
    #                     sent_message = bot13.send_message(botChatIdw, order_info, reply_markup=markup2, parse_mode='html')
    #                     last_message_id = sent_message.message_id  


    #                     user_chat_id_str = user_chat_ids.get(user_id_mess, "")
    #                     if user_chat_id_str:
    #                         user_chat_id_str += ","
    #                     user_chat_id_str += str(botChatIdw)
    #                     user_chat_ids[user_id_mess] = user_chat_id_str

    #                     user_message_id_list = user_message_ids.get(user_id_mess, [])
    #                     # Добавляем новый message_id
    #                     user_message_id_list.append(last_message_id)
    #                     # Сохраняем обновленный список в словаре
    #                     user_message_ids[user_id_mess] = user_message_id_list
    #                     # Добавляем новый message_id
    #                     last_message_id_str = str(last_message_id)
    #                     current_message_ids.append(last_message_id_str)
                            
    #                     # Преобразуем обновленный список в строку
    #                     updated_message_ids_str = ','.join(current_message_ids)
    #             cur5.close()
    #             conn5.close()   

    #             for user_id_mess, message_id_list in user_message_ids.items():
    #                 updated_message_ids_str = ','.join(map(str, message_id_list))
    #                 sql_query = "UPDATE orders SET orderMessageId = ('%s'), orderChatId = ('%s') WHERE id = ('%s')"
    #                 cur.execute(sql_query % (updated_message_ids_str, user_chat_id_str, user_id_mess))

    #             # Коммит изменений в базу данных
    #             conn.commit()
    #             last_sent_message = order_info
    #             check_mess_already_send = False                    
    #         else:
    #             print('Нет новых сообщений')
    #             print(user_last_message_ids)

    #     else:                
    #         print('Заказов пока нет, но скоро будут')       
    #     cur.close()
    #     conn.close()
    # except sqlite3.Error as e:
    #     if not error_reported:
                
    #         print('Заказов пока нет, но скоро будут')
    #         error_reported = True  # Устанавливаем флаг ошибки, чтобы сообщение выводилось только один раз
    
    #     conn.close()
# Функция для отправки клавиатуры с фамилиями клиентов
def send_customers_keyboard(message):
    global offset
    conn = sqlite3.connect('custumers.sql')
    cursor = conn.cursor()
    cursor.execute('SELECT last_name, firts_name, middle_name FROM custumers LIMIT 10 OFFSET ?', (offset,))
    customers = cursor.fetchall()

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for customer in customers:
        keyboard.add(f"{customer[0]} {customer[1]} {customer[2]}")

    # Добавление кнопок "Назад", "Вперед" и "Закрыть"
    control_buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    control_buttons.row(telebot.types.KeyboardButton("Назад"), telebot.types.KeyboardButton("Вперед"), telebot.types.KeyboardButton("Закрыть"))
    keyboard.add(control_buttons.row)

    bot13.send_message(message.chat.id, "Выберите клиента:", reply_markup=keyboard)
    conn.close()

# Обработчик текстовых сообщений
@bot13.message_handler(func=lambda message: True)
def handle_text(message):
    global offset
    if message.text == 'Закрыть':
        bot13.send_message(message.chat.id, "Закрытие базы данных...")
        bot13.send_message(message.chat.id, "База данных успешно закрыта.")
    elif message.text == 'Назад':
        # Отправка предыдущих 10 записей
        offset = max(0, offset - 10)
        send_customers_keyboard(message)
    elif message.text == 'Вперед':
        # Отправка следующих 10 записей
        offset += 10
        send_customers_keyboard(message)

@bot13.callback_query_handler(func=lambda callback: callback.data == orderSendTextCallbackData)
@bot13.callback_query_handler(func=lambda callback: callback.data == orderDeleteCallbackData) 
def callback_message_created_order(callback):  
    global feedback 
    global chatcity
    
    if callback.data == orderSendTextCallbackData:
        feedback = orderSendText     

        application = f'✅\n<b>·{cityname}: </b>{needText} {countPeople} {humanCount}\n<b>·Адрес:</b>👉 {adress}\n<b>·Что делать:</b> {whattodo}\n<b>·Начало работ:</b> в {timetostart}\n<b>·Вам на руки:</b> <u>{salary}.00</u> р./час, минималка 2 часа\n<b>·Приоритет самозанятым</b>' 
        
        markup1 = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('❌ Закрыть заявку', callback_data='❌ Закрыть заявку', one_time_keyboard=True)
        markup1.row(btn01)
        bot13.edit_message_text(application, callback.message.chat.id, callback.message.message_id, reply_markup=markup1, parse_mode='html')

        print(sent_message_id)
        if cityname == 'Арзамас':
            chatcity = arzCity
        elif cityname == 'Екатеринбург':                    
            chatcity = ekaCity
        elif cityname == 'Санкт-Петербург':                    
            chatcity = sanCity           
        elif cityname == 'Москва':
            chatcity = mosCity
    else:          
        feedback = orderDeleteText
        bot13.delete_message(callback.message.chat.id, callback.message.message_id)
    
    import_into_database(callback.message)

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

@bot13.message_handler(content_types=['text'])
def check_callback_message_ready_order(message):          
        global state      
        if state == 'initial':         
            bot13.edit_message_text(userCitizenRuText, message.chat.id, message.message_id-1)
            bot13.send_message(message.chat.id, userCitizenRuError, parse_mode='html')
            # created_order(message)         
        elif state == 'citizenRU':
            bot13.send_message(message.chat.id, orderSucsess, parse_mode='html')
            import_into_database(message)
        else:
            bot13.edit_message_text(userCitizenRuText, message.chat.id, message.message_id)

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
    bot13.send_message(message.chat.id, alreadyRegistered, reply_markup=markup)    
    state = 'citizenRU'
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

        bot13.send_message(message.chat.id, info)
        print(info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
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

        bot13.send_message(message.chat.id, info)
        print(info)
    else:
        bot13.send_message(message.chat.id, 'Введите логин и пароль прежде чем продолжить работу')
        input_admin(message)

def show_database_userOrder(message):
    print(loginin)
    if loginin == True:

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
print("testfromiphone")