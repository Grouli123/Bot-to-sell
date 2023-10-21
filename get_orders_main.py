import telebot
from telebot import types
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime
import time

import re

import  get_orders_config.get_orders_API_key as API_key
# import get_orders_config.get_orders_sqlBase as sqlBase
import  get_orders_config.get_orders_config_message as config_message


botApiKey = API_key.botAPIArz

bot = telebot.TeleBot(botApiKey)

# base = sqlBase.createDatabase
# insertIntoBase = sqlBase.insertIntoDatabase
# nameOfBase = sqlBase.name_of_base

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
# test = False
# test2 = None
orderTakeTwo = ''


fioFirstFriend = None
fioSecondFriend = None
fioThirdFriend = None


phoneNumberFirstFriend = None
phoneNumberSecondFriend = None
phoneNumberThirdFriend = None

checkThirdFriend = False
checkFourthFriend = False

@bot.message_handler(commands=['start'])
def registration(message):
    global check_mess_already_send
    global user_id
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

    # global orderTakeTwo
    global user_id_mess

    # global test
    # global test2
    data_called = False

    # conn = sqlite3.connect('user_data.sql')
    # cursor = conn.cursor()

    # cursor.execute('''CREATE TABLE IF NOT EXISTS users
    # (user_id INTEGER PRIMARY KEY, username TEXT)''')
    # conn.commit()
    
    user_id = message.from_user.id
    # username = message.from_user.username

    

  
    
    # cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES ('%s', '%s')" % (user_id, username))
    # conn.commit()
    # conn.close()

    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
          # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки
    
    if takeParam:
        check_user_id = takeParam[9]

    else:
        check_user_id = None
    conn.close()

    if check_user_id is not None or user_id is not None:
        bot.send_message(message.chat.id, f'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажам на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на твоей клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
        userCitizenRuText = f'👉Пока можешь почитать отзывы о нашей организации'
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
        bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)

    while True:
       
        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()

        try:
            cur.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 1')
            users = cur.fetchone() 

            

            
            if users is not None:
                if (int(users[3]) <= 1) or (int(users[3]) >= 5):
                    humanCount = 'человек'
                else:
                    humanCount = 'человека'
                    
                if int(users[3]) > 1:
                    needText = 'Нужно'
                else:
                    needText = 'Нужен'

                if (int(users[3]) <= 1):
                    markup2 = types.InlineKeyboardMarkup()
                    btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                    btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                    markup2.row(btn12)  
                    markup2.row(btn52)            
                elif (int(users[3]) == 2):
                    markup2 = types.InlineKeyboardMarkup()
                    btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                    btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
                    btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                    markup2.row(btn12)  
                    markup2.row(btn22)  
                    markup2.row(btn52) 
                elif (int(users[3]) == 3):
                    markup2 = types.InlineKeyboardMarkup()
                    btn12 = types.InlineKeyboardButton('Еду 1', callback_data='Еду 1', one_time_keyboard=True)
                    btn22 = types.InlineKeyboardButton('Едем в 2', callback_data='Едем в 2', one_time_keyboard=True)
                    btn32 = types.InlineKeyboardButton('Едем в 3', callback_data='Едем в 3', one_time_keyboard=True)
                    btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                    markup2.row(btn12)  
                    markup2.row(btn22)  
                    markup2.row(btn32)  
                    markup2.row(btn52) 
                elif (int(users[3]) >= 4):
                    markup2 = types.InlineKeyboardMarkup()
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
            
                
                # print(users[10])
                order_info = f'✅\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n<b>•Адрес:</b>👉 {users[4]}\n<b>•Что делать:</b> {users[5]}\n<b>•Начало работ:</b> {users[6]}\n<b>•Вам на руки:</b> <u>{users[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
                # if str(users[10]) == "False" and check_mess_already_send == False:    
                    # print(users[10])      
                    # order_info_close = f'❌ Заявка закрыта\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n<b>•Адрес:</b>👉 {users[4]}\n<b>•Что делать:</b> {users[5]}\n<b>•Начало работ:</b> {users[6]}\n<b>•Вам на руки:</b> <u>{users[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
                    # previos_mes = users[9]
                    # print(previos_mes)
                                       

                    

                    # for user_id_mess in user_message_ids.keys():
                    #     cursor.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % user_id_mess)
                    #     order_message_id_str = cursor.fetchone()[0]

                    #     # Разбейте строку orderMessageId на список message_id
                    #     message_id_list = order_message_id_str.split(',') if order_message_id_str else []

                    #     # Измените сообщение для каждого message_id
                    #     for message_id in message_id_list:
                    #         # print(message_id)
                    #         bot.edit_message_text(order_info_close, message.chat.id, message_id, parse_mode='html')

                    # # Закрытие соединения с базой данных
                    # conn.close()

                    # bot.edit_message_text(order_info_close, message.chat.id, previos_mes, parse_mode='html')
                    # last_message_id = None
                    # last_sent_message = None
                    # print('работает иф')
                    # check_mess_already_send = True
                
                if order_info != last_sent_message:
                    
                    print('работает елсе')
                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()

                     # Получаем ID пользователя
                    user_id_mess = users[0]
                    # test2 = users[0]
                    # Получаем текущий список message_id из базы данных
                    cursor.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % (user_id_mess))
                    current_message_ids_str = cursor.fetchone()[0]
                    
                    # Преобразуем текущую строку в список (если она не пуста)
                    current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []
                    
                    # user_last_message_ids[user_id_mess] = last_message_id
                    # # Проверяем, есть ли уже запись для этого пользователя в словаре
                    # if user_id_mess in user_last_message_ids:
                    #     user_last_message_ids[user_id_mess].append(last_message_id)
                    # else:
                    #     user_last_message_ids[user_id_mess] = [last_message_id]
                    messageChatId = message.chat.id
                    sent_message = bot.send_message(messageChatId, order_info, reply_markup=markup2, parse_mode='html')
                    last_message_id = sent_message.message_id  

                    # user_chat_id_list = user_chat_ids.get(user_id_mess, [])
                    # user_chat_id_list.append(test)
                    # user_chat_ids[user_id_mess] = user_chat_id_list

                    user_chat_id_str = user_chat_ids.get(user_id_mess, "")
                    if user_chat_id_str:
                        user_chat_id_str += ","
                    user_chat_id_str += str(messageChatId)
                    user_chat_ids[user_id_mess] = user_chat_id_str

                    user_message_id_list = user_message_ids.get(user_id_mess, [])
                    # Добавляем новый message_id
                    user_message_id_list.append(last_message_id)
                    # Сохраняем обновленный список в словаре
                    user_message_ids[user_id_mess] = user_message_id_list
                    # Добавляем новый message_id
                    last_message_id_str = str(last_message_id)
                    current_message_ids.append(last_message_id_str)
                    
                    # Преобразуем обновленный список в строку
                    updated_message_ids_str = ','.join(current_message_ids)
                    # print('не должен равняться NONE ', last_message_id) #работает
                    

                    
                    # conn = sqlite3.connect('applicationbase.sql')
                    # cursor = conn.cursor()
                    # if test is True:
                    #     cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                    #     takeParam3 = cursor2.fetchone() # Получение первой соответствующей строки

                    #     test = False

                
                    for user_id_mess, message_id_list in user_message_ids.items():
                        updated_message_ids_str = ','.join(map(str, message_id_list))
                        # sql_query = "UPDATE orders SET orderMessageId = ('%s') WHERE id = ('%s')"
                        # cursor.execute(sql_query % (updated_message_ids_str, user_id_mess))
                        sql_query = "UPDATE orders SET orderMessageId = ('%s'), orderChatId = ('%s') WHERE id = ('%s')"
                        cursor.execute(sql_query % (updated_message_ids_str, user_chat_id_str, user_id_mess))

                    # Коммит изменений в базу данных
                    conn.commit()

                    # # Закрытие соединения с базой данных
                    # conn.close()
                    # conn = sqlite3.connect('applicationbase.sql')
                    # cursor = conn.cursor()
                    # for user_id_mess, chat_id_list in user_chat_ids.items():
                    #     updated_chat_id_str = ','.join(map(str, chat_id_list))
                    #     sql_query = "UPDATE orders SET orderChatId = ('%s') WHERE id = ('%s')"
                    #     cursor.execute(sql_query % (updated_chat_id_str, user_id_mess))

                    

                    

                    # sql_query = "UPDATE orders SET orderMessageId = ('%s') WHERE id = ('%s')"
                    # cursor.execute(sql_query % (updated_message_ids_str , user_id_mess))
                    # print('мессадже айди ', user_id_mess)

                    # # Коммит изменений в базу данных
                    # conn.commit()

                    # # Закрытие соединения с базой данных
                    # conn.close()
                    # print('апдейт мессадже ',updated_message_ids_str)

                    # print(last_message_id)                  
                    last_sent_message = order_info
                    check_mess_already_send = False




                    # conn2 = sqlite3.connect('peoplebase.sql')
                    # cursor2 = conn2.cursor()
                    #     # Запрос к базе данных для поиска строки по значению переменной
                    # # cursor2.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                    
                    
                    # if test is True:
                    # #     cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                    # #     takeParam3 = cursor2.fetchone() # Получение первой соответствующей строки
                    #     cur.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (test2, user_id))
                    #     takeParam2 = cursor2.fetchone() # Получение первой соответствующей строки

                    #     test = False

                    # if takeParam2:
                    #     orderTakeTwo = takeParam2[15]
                    # else:
                    #     print('не работает')
                    # conn2.commit()

                    # conn2.close()



                    
                else:
                    print('Нет новых сообщений')
                    print(user_last_message_ids)

            else:
                # bot.send_message(message.chat.id, 'Заказов пока что нет, но они скоро появятся')  
                
                print('Заказов пока нет, но скоро будут')
       

        # info = ''
        # for el in users:
        #     info += f'Заявка номер: {el[0]}, Дата создания: {el[1]}, Город: {el[2]}, Количество людей: {el[3]}, Адрес: {el[4]}, Что делать: {el[5]}, Начало работ: {el[6]}, Вам на руки: {el[7]}\n\n'
        

        # bot.send_message(message.chat.id, order_info)
        # print(order_info)
            cur.close()
            conn.close()
            time.sleep(3)
        except sqlite3.Error as e:
            # Обработка ошибки, если таблицы нет или произошла другая ошибка
            if not error_reported:
                # bot.send_message(message.chat.id, f'Заказов пока нет, но скоро будут', parse_mode='html')
                
                print('Заказов пока нет, но скоро будут')
                error_reported = True  # Устанавливаем флаг ошибки, чтобы сообщение выводилось только один раз
    
            # Закрытие соединения с базой данных
            conn.close()
        # finally:
        #     # Закрытие соединения с базой данных
        #     conn.close()

    
@bot.callback_query_handler(func=lambda callback: callback.data == 'Еду 1')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 2') 
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 3')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 4')
def callback_data_of_data(callback): 
    global orderTakeTwo
    global checkThirdFriend
    global checkFourthFriend
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    # cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (user_id_mess, user_id))
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam2 = cursor.fetchone() # Получение первой соответствующей строки
    if takeParam2:
        orderTakeTwo = takeParam2[0]
    else:
        print('не работает')

    if callback.data == 'Еду 1':
        
        
        cursor.execute("SELECT orderTake FROM users WHERE user_id = ('%s')" % (user_id))
        takeOrderTake = cursor.fetchone()

        if takeOrderTake is not None:
            current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""

            new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
            cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (new_orderId, user_id))

        conn.commit()
        cursor.close()
        conn.close()

        # conn2 = sqlite3.connect('applicationbase.sql')
        # cursor2 = conn2.cursor()        

        # cursor2.execute("SELECT whoTakeId FROM orders WHERE id = ('%s')" % (user_id_mess))
        # current_values = cursor2.fetchone()

        # current_phone_numbers = current_values[0] if current_values[0] else ""
        # new_phone_numbers = current_phone_numbers + "," + phoneNumberSecondFriend if current_phone_numbers else phoneNumberSecondFriend

        # cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (new_phone_numbers, user_id_mess))


        # # cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (orderTakeTwo, user_id_mess))
        # conn2.commit()
        # cursor2.close()
        # conn2.close()

        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        

        cursor2.execute("SELECT whoTakeId FROM orders WHERE id = ('%s')" % (user_id_mess))
        current_values = cursor2.fetchone()

        if current_values is not None:
            current_phone_numbers = current_values[0] if current_values[0] else ""
            print(type(current_phone_numbers))
            new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo

            cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (new_phone_numbers, user_id_mess))

        conn2.commit()
        cursor2.close()
        conn2.close()

        # conn = sqlite3.connect('applicationbase.sql')
        # cursor = conn.cursor()

        # cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE id = ('%s')" % (user_id_mess))
        # current_values = cursor.fetchone()

        # current_phone_numbers = current_values[0] if current_values[0] else ""
        # current_fio = current_values[1] if current_values[1] else ""
                
        # new_phone_numbers = current_phone_numbers + "," + phoneNumberSecondFriend if current_phone_numbers else phoneNumberSecondFriend
        # new_fio = current_fio + "," + fioSecondFriend if current_fio else fioSecondFriend

        # # cursor.execute("UPDATE orders SET numberPhoneFriends = ?, FIOFriends = ? WHERE id = ?", (new_phone_numbers, new_fio, user_id_mess))
                

        # cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE id = '%s'" % (new_phone_numbers, new_fio, user_id_mess))

        # # cursor2.execute("SELECT orderMessageId FROM orders WHERE user_id = ('%s')" % (user_id))
        # conn.commit()
        # cursor.close()
        # conn.close()
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        

        cursor2.execute("SELECT * FROM orders WHERE id = ('%s')" % (user_id_mess))
        table_element = cursor2.fetchone()

        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

        bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}') 
        conn2.commit()
        cursor2.close()
        conn2.close()
    elif callback.data == 'Едем в 2':
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        

        cursor2.execute("SELECT * FROM orders WHERE id = ('%s')" % (user_id_mess))
        table_element = cursor2.fetchone()

        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

        # bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}') 
        conn2.commit()
        cursor2.close()
        conn2.close()
        input_fio_first_friend(callback.message)

    elif callback.data == 'Едем в 3':
        checkThirdFriend = True
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        

        cursor2.execute("SELECT * FROM orders WHERE id = ('%s')" % (user_id_mess))
        table_element = cursor2.fetchone()

        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

        # bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}') 
        conn2.commit()
        cursor2.close()
        conn2.close()
        input_fio_first_friend(callback.message)
        # bot.send_message(callback.message.chat.id, 'Принято, вы едете в 3')
    elif callback.data == 'Едем в 4':         
        checkThirdFriend = True
        checkFourthFriend = True       
        conn2 = sqlite3.connect('applicationbase.sql')
        cursor2 = conn2.cursor()        

        cursor2.execute("SELECT * FROM orders WHERE id = ('%s')" % (user_id_mess))
        table_element = cursor2.fetchone()

        order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

        bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

        # bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}') 
        conn2.commit()
        cursor2.close()
        conn2.close()
        input_fio_first_friend(callback.message)
        # bot.send_message(callback.message.chat.id, 'Принято, вы едете в 4')

def input_fio_first_friend(message):
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
            input_first_friend_number(message)

def input_first_friend_number(message):
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
                    input_fio_second_friend(message)           
                    print(checkThirdFriend)
                else:  

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

                        cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (new_phone_numbers, user_id_mess))

                    conn2.commit()
                    cursor2.close()
                    conn2.close()



                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()

                    cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE id = ('%s')" % (user_id_mess))
                    current_values = cursor.fetchone()

                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    current_fio = current_values[1] if current_values[1] else ""
                    
                    new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend if current_phone_numbers else phoneNumberFirstFriend
                    new_fio = current_fio + "," + fioFirstFriend if current_fio else fioFirstFriend

                    # cursor.execute("UPDATE orders SET numberPhoneFriends = ?, FIOFriends = ? WHERE id = ?", (new_phone_numbers, new_fio, user_id_mess))
                    

                    cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE id = '%s'" % (new_phone_numbers, new_fio, user_id_mess))

                    # cursor2.execute("SELECT orderMessageId FROM orders WHERE user_id = ('%s')" % (user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    

                    bot.send_message(message.chat.id, f'Вы {lastname} {firstname} {middlename} номер телефона: {nuberPhone} едете с другом: {fioFirstFriend} номер телефона: {phoneNumberFirstFriend}', parse_mode='html')
                

                    print('Номер телефона друга: ', phoneNumberFirstFriend, 'ФИО друга: ', fioFirstFriend)

               
                
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_first_friend_number(message)

def input_fio_second_friend(message):
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
            message.text.strip(None)
            input_fio_second_friend(message) 
        else:
            fioSecondFriend = message.text.strip()
            print(fioSecondFriend)
            input_second_friend_number(message)

def input_second_friend_number(message):
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
            message.text.strip(None)
            input_second_friend_number(message)        
        else:               
            if message.text.isdigit():
                phoneNumberSecondFriend = message.text.strip()    
                if checkFourthFriend is True:      
                    checkFourthFriend = False
                    input_fio_third_friend(message)              
                    print(checkFourthFriend)
                else:
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

                        cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (new_phone_numbers, user_id_mess))

                    conn2.commit()
                    cursor2.close()
                    conn2.close()


                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()

                    cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE id = ('%s')" % (user_id_mess))
                    current_values = cursor.fetchone()

                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    current_fio = current_values[1] if current_values[1] else ""
                    new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend + "," + phoneNumberSecondFriend if current_phone_numbers else phoneNumberFirstFriend + "," + phoneNumberSecondFriend
                    new_fio = current_fio + "," + fioFirstFriend + "," + fioSecondFriend if current_fio else fioFirstFriend + "," + fioSecondFriend

                    # cursor.execute("UPDATE orders SET numberPhoneFriends = ?, FIOFriends = ? WHERE id = ?", (new_phone_numbers, new_fio, user_id_mess))
                    

                    cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE id = '%s'" % (new_phone_numbers, new_fio, user_id_mess))

                    # cursor2.execute("SELECT orderMessageId FROM orders WHERE user_id = ('%s')" % (user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    

                    bot.send_message(message.chat.id, f'Вы {lastname} {firstname} {middlename} номер телефона: {nuberPhone}.\nВаши друзья:\n1. {fioFirstFriend} номер телефона: {phoneNumberFirstFriend}\n2. {fioSecondFriend} номер телефона: {phoneNumberSecondFriend}', parse_mode='html')


                    print('Номер телефона друга: ', phoneNumberSecondFriend, 'ФИО друга: ', fioSecondFriend)

                
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_second_friend_number(message)

def input_fio_third_friend(message):
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
            message.text.strip(None)
            input_fio_third_friend(message) 
        else:
            fioThirdFriend = message.text.strip()
            print(fioThirdFriend)
            input_third_friend_number(message)

def input_third_friend_number(message):
    bot.send_message(message.chat.id, 'Введите номер телефона третьего друга:', parse_mode='html')
    bot.register_next_step_handler(message, third_friend_number_check)

def third_friend_number_check(message):   
    global phoneNumberThirdFriend
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_third_friend_number(message)
    else:
        if len(message.text.strip()) != 11:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона')
            message.text.strip(None)
            input_third_friend_number(message)        
        else:               
            if message.text.isdigit():
                phoneNumberThirdFriend = message.text.strip()    

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
                print(user_id_mess)
                if current_values is not None:
                    current_phone_numbers = current_values[0] if current_values[0] else ""
                    print(type(current_phone_numbers))
                    new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo

                    cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE id = '%s'" % (new_phone_numbers, user_id_mess))

                conn2.commit()
                cursor2.close()
                conn2.close()



                conn = sqlite3.connect('applicationbase.sql')
                cursor = conn.cursor()

                cursor.execute("SELECT numberPhoneFriends, FIOFriends FROM orders WHERE id = ('%s')" % (user_id_mess))
                current_values = cursor.fetchone()

                current_phone_numbers = current_values[0] if current_values[0] else ""
                current_fio = current_values[1] if current_values[1] else ""


                # new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend + "," + phoneNumberSecondFriend if current_phone_numbers else phoneNumberSecondFriend
                # new_fio = current_fio + "," + fioFirstFriend + "," + fioSecondFriend if current_fio else fioSecondFriend

                
                new_phone_numbers = current_phone_numbers + "," + phoneNumberFirstFriend + "," + phoneNumberSecondFriend + "," + phoneNumberThirdFriend if current_phone_numbers else phoneNumberFirstFriend + "," + phoneNumberSecondFriend + "," + phoneNumberThirdFriend
                new_fio = current_fio + "," + fioFirstFriend + "," + fioSecondFriend + "," + fioThirdFriend if current_fio else fioFirstFriend + "," + fioSecondFriend + "," + fioThirdFriend

                # cursor.execute("UPDATE orders SET numberPhoneFriends = ?, FIOFriends = ? WHERE id = ?", (new_phone_numbers, new_fio, user_id_mess))
                

                cursor.execute("UPDATE orders SET numberPhoneFriends = '%s', FIOFriends = '%s' WHERE id = '%s'" % (new_phone_numbers, new_fio, user_id_mess))

                # cursor2.execute("SELECT orderMessageId FROM orders WHERE user_id = ('%s')" % (user_id))
                conn.commit()
                cursor.close()
                conn.close()
                
                bot.send_message(message.chat.id, f'Вы {lastname} {firstname} {middlename} номер телефона: {nuberPhone}.\nВаши друзья:\n1.{fioFirstFriend} номер телефона: {phoneNumberFirstFriend}\n2. {fioSecondFriend} номер телефона: {phoneNumberSecondFriend}\n 3. {fioThirdFriend} номер телефона: {phoneNumberThirdFriend}', parse_mode='html')

                # bot.send_message(message.chat.id, f'Вы {lastname} {firstname} {middlename} номер телефона: {nuberPhone} едете с другом: {fioThirdFriend} номер телефона: {phoneNumberThirdFriend}', parse_mode='html')
                

                print('Номер телефона друга: ', phoneNumberFirstFriend, 'ФИО друга: ', fioFirstFriend)
                print('Номер телефона друга: ', phoneNumberSecondFriend, 'ФИО друга: ', fioSecondFriend)
                print('Номер телефона друга: ', phoneNumberThirdFriend, 'ФИО друга: ', fioThirdFriend)
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_third_friend_number(message)




@bot.message_handler(commands=['data'])
def data(message):
    global user_id

    global city

    
    global cityTrue

    global nuberPhone
    global city
    global lastname
    global firstname
    global middlename
    global dataOfBirth       
    global citizenRF 
    global id_nubmer_list

    global check_user_id
    

    global data_called

    global nalogacc
    global passport

    global samozanYorN

    global orderTake
    global orderDone
    global orderMiss

    global percent_completed
    global percent_failed

    # conn = sqlite3.connect('user_data.sql')
    # cursor = conn.cursor()

    # cursor.execute('''CREATE TABLE IF NOT EXISTS users
    # (user_id INTEGER PRIMARY KEY, username TEXT)''')
    # conn.commit()
    
    user_id = message.from_user.id
    # username = message.from_user.username
    
    # cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES ('%s', '%s')" % (user_id, username))
    # conn.commit()
    # conn.close()
    if not data_called:  # Если data не вызывалась в предыдущий раз

            # Подключение к базе данных SQLite
        conn = sqlite3.connect('peoplebase.sql')
        cursor = conn.cursor()

            # Запрос к базе данных для поиска строки по значению переменной
        cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
        takeParam = cursor.fetchone() # Получение первой соответствующей строки
        
        if takeParam:
            check_user_id = takeParam[9]
        else:
            check_user_id = None
        conn.close()
        
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
            print('Значение не найдено') # Сообщение, если значение не найдено

            # Закрытие соединения с базой данных
        conn.close()
        if nalogacc == 'Нет':
            samozanYorN = 'Нет'
        elif passport != 'Нет':
            samozanYorN = f'Да\n💰 Р/С: {nalogacc}\n🪪 Паспорт: {passport}'
        else:
            samozanYorN = f'Да\n💰 Р/С: {nalogacc}'

        if check_user_id is not None or user_id is not None:
            if  cityTrue == 'False':
                markup = types.InlineKeyboardMarkup()
                btn2 = types.InlineKeyboardButton('🖌Редактировать город', callback_data='🖌Редактировать город', one_time_keyboard=True)
                btn3 = types.InlineKeyboardButton('✅Подтвердить', callback_data='✅Подтвердить', one_time_keyboard=True)
                markup.row(btn2)  
                markup.row(btn3)  
                bot.send_message(message.chat.id, f'📞 Телефон: +{nuberPhone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {dataOfBirth}\n🇷🇺 Гражданство РФ: {citizenRF}\n🤝 Самозанятый: {samozanYorN} \n🏙 Город(а): {city}\n\nℹ️ Чтобы выйти из этого меню нажмите ✅Подтвердить', reply_markup=markup)
                print('первый иф',check_user_id, 'продолжение', user_id)
            else:
                # user_id = message.from_user.id
                # username = message.from_user.username
                
                # cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES ('%s', '%s')" % (user_id, username))
                # conn.commit()
                # conn.close()
                
                #     # Подключение к базе данных SQLite
                # conn = sqlite3.connect('peoplebase.sql')
                # cursor = conn.cursor()

                #     # Запрос к базе данных для поиска строки по значению переменной
                # cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
                # takeParam = cursor.fetchone() # Получение первой соответствующей строки
                
                # if takeParam:
                #     check_user_id = takeParam[9]
                # else:
                #     check_user_id = None
                # conn.close()
                
                # if takeParam:
                #     id_nubmer_list = takeParam[0]
                #     nuberPhone = takeParam[2]
                #     city = takeParam[3]
                #     lastname = takeParam[4]
                #     firstname = takeParam[5]
                #     middlename = takeParam[6]
                #     dataOfBirth = takeParam[7]        
                #     citizenRF = takeParam[8]   
                #     cityTrue = takeParam[14]  
                #     print('робит2', cityTrue)

                # else:
                #     print('Значение не найдено') # Сообщение, если значение не найдено

                #     # Закрытие соединения с базой данных
                # conn.close()
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
                print('первый элс',check_user_id, 'продолжение', user_id)
        else:
            print('второй иф',check_user_id, 'продолжение', user_id)
            markup = types.InlineKeyboardMarkup()
            btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
            markup.row(btn2)          
            bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)
        data_called = True  # Устанавливаем флаг в True
    else:
        bot.send_message(message.chat.id, 'Функция data уже была вызвана. Повторный вызов невозможен.')




@bot.message_handler(commands=['orders'])
def orders(message):

    global check_user_id
    
    global data_called
    data_called = False
    # conn = sqlite3.connect('user_data.sql')
    # cursor = conn.cursor()

    # cursor.execute('''CREATE TABLE IF NOT EXISTS users
    # (user_id INTEGER PRIMARY KEY, username TEXT)''')
    # conn.commit()
    
    user_id = message.from_user.id
    # username = message.from_user.username
    
    # cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES ('%s', '%s')" % (user_id, username))
    # conn.commit()
    # conn.close()
    
        # Подключение к базе данных SQLite
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()

        # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки
    
    if takeParam:
        check_user_id = takeParam[9]
    else:
        check_user_id = None
    conn.close()
    if check_user_id is not None or user_id is not None:

        conn = sqlite3.connect('applicationbase.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE id = ('%s')" % (user_id_mess))
        users = cur.fetchall()
        info = ''
        for el in users:
            info += f'Вы взяли заказ номер: {el[0]}\n<b>•Город:</b> {el[2]}\n<b>•Адрес:</b>👉 {el[4]}\n<b>•Что делать:</b> {el[5]}\n<b>•Начало работ:</b> в {el[6]}\n<b>•Вам на руки:</b> <u>{el[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
        cur.close()
        conn.close()

        bot.send_message(message.chat.id, info, parse_mode='html')

        # usercitizenRF = 'На данный момент у Вас нет активных заявок. Следите за новыми заявками и берите те, по которым хотите работать.'   
        # bot.send_message(message.chat.id, usercitizenRF)
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)          
        bot.send_message(message.chat.id, f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)



def input_birtgday(message):
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



@bot.callback_query_handler(func=lambda callback: callback.data == '📝Редактировать данные')
@bot.callback_query_handler(func=lambda callback: callback.data == '📊 Статистика заказов') 
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Подтвердить аккаунт')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅Самозанятость')
def callback_data_of_data(callback): 
    global cityTrue
    global isOpenEdit
    global data_called
    global samozanYorN

    global percent_completed
    global percent_failed
    if callback.data == '📝Редактировать данные':
        data_called = False
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cityTrue = 'False'
        conn = sqlite3.connect('peoplebase.sql')
        cur = conn.cursor()
        cur.execute("UPDATE users SET  cityAgree = '%s' WHERE id = '%s'" % (cityTrue, id_nubmer_list))
        conn.commit() 
        cur.close()
        conn.close()
        print('сити тру ',cityTrue)

        data(callback.message)

    elif callback.data == '📊 Статистика заказов':  
        data_called = False         
        conn = sqlite3.connect('peoplebase.sql')
        c = conn.cursor()

        # Выполнение SQL-запроса
        # c.execute("SELECT orderTake, orderDone, orderMiss FROM users")
        c.execute("SELECT * FROM users WHERE id = '%s'" % (id_nubmer_list))
        test2 = c.fetchone()
        # Получение данных
        orderDataTake = test2[15]
        orderDataDone = test2[16]
        orderDataMiss = test2[17]

        # Разделение данных по запятым и подсчет количества записей
        recordsTake = orderDataTake.split(',')
        orderCountTake = len(recordsTake)

        recordsDone = orderDataDone.split(',')
        orderCountDone = len(recordsDone)

        recordsMiss = orderDataMiss.split(',')
        orderCountMiss = len(recordsMiss)

        print(f"Количество записей: {orderCountTake}")
        print(f"Количество записей: {orderCountDone}")
        print(f"Количество записей: {orderCountMiss}")

        # Закрытие соединения с базой данных
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
        print(nuberPhone , lastname)
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

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Да, официально зареган')
@bot.callback_query_handler(func=lambda callback: callback.data == '☑️ Нет, хочу зарегистрироваться')
@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Нет, пропустить')
def callback_individual(callback): 
    global editButtonText1
    global editButtonText2
    global editButtonText3
    

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
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('➡️ Пропустить', callback_data='➡️ Пропустить2', one_time_keyboard=True)
    markup.row(btn2)  
    bot.send_message(message.chat.id, 'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, my_nalog_accaunt_check)   

def my_nalog_accaunt_check(message):
    global nalogacc
    if message.text is None:
        bot.send_message(message.from_user.id, textOnly)
        input_my_nalog_accaunt(message) 
    else:
        if len(message.text.strip()) != 20:
            bot.send_message(message.chat.id, 'Введите корректный номер счета')
            message.text.strip(None)
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
                message.text.strip(None)
                input_my_nalog_accaunt(message) 

# работаю тут
@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Пропустить2')
def callback_bank(callback):
    if callback.data == '➡️ Пропустить2': 
        bot.edit_message_text(f'Введите Ваш номер счёта (20 цифр, не номер карты, смотреть в реквизитах)', callback.message.chat.id, callback.message.message_id)
        data(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText1)
@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText2)
@bot.callback_query_handler(func=lambda callback: callback.data == editButtonText3)
def callback_bank(callback): 
    
    global editButtonText1
    global editButtonText2
    global editButtonText3
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
        bot.edit_message_text(f'В приложении СберБанк Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)   
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
        bot.edit_message_text(f'В приложении Тинькофф Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
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
        bot.edit_message_text(f'В приложении Другой банк Онлайн\n1. Откройте СберБанк Онлайн на телефоне\n2. Откройте «Настройки» или «Каталог», затем найдите раздел «Сервисы и услуги»\n3. Нажмите на пункт «Своё дело», далее «Подключить сервис»\n4. Выберите Дебетовую карту и введите данные (Номер телефона, Регион деятельности, Вид деятельности «ООО»\n5. Далее «Условия подключения» поставьте галочку и нажмите продолжить\n6. Затем дождитесь СМС о подключении сервиса «Своё дело» от СберБанка, затем СМС от налоговой.\n\nДля более подробной инструкции, переходи по ссылке https://www.sberbank.ru/ru/svoedelo#freeservices\n\nПрошел процедуру регистрации? Жми кнопку "Продолжить"', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
   


@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Продолжить')
def callback_edit_data_person(callback): 
    if callback.data == '➡️ Продолжить':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        
        
    #     bot.send_message(callback.message.chat.id, f'Сначала необходимо подтвердить паспортные данные!', parse_mode='html')

    #     markup = types.InlineKeyboardMarkup()
    #     btn1 = types.InlineKeyboardButton('🖌Редактировать ФИО', callback_data='🖌Редактировать ФИО', one_time_keyboard=True)
    #     btn2 = types.InlineKeyboardButton('🖌Редактировать дату рождения',callback_data='🖌Редактировать ДР', one_time_keyboard=True)
    #     btn3 = types.InlineKeyboardButton('🖌Редактировать паспорт', callback_data='🖌Редактировать ПС', one_time_keyboard=True)        
    #     btn4 = types.InlineKeyboardButton('✅ Подтвердить(Осталось попыток:2)', callback_data='✅ Подтвердить', one_time_keyboard=True)
    #     btn5 = types.InlineKeyboardButton('➡️ Пропустить, остаться с низким приоритетом', callback_data='➡️ Пропустить', one_time_keyboard=True)

    #     markup.row(btn1)
    #     markup.row(btn2)
    #     markup.row(btn3)
    #     markup.row(btn4)
    #     markup.row(btn5)
    #     bot.send_message(callback.message.chat.id, f'ФИО: <u>{lastname} {firstname} {middlename}</u>\nДата рождения: {dataOfBirth}\nСерия и номер паспорта: {passport}', parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ФИО')
@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ДР')
@bot.callback_query_handler(func=lambda callback: callback.data == '🖌Редактировать ПС')
@bot.callback_query_handler(func=lambda callback: callback.data == '✅ Подтвердить')
@bot.callback_query_handler(func=lambda callback: callback.data == '➡️ Пропустить')
def callback_edit_person_data_alone(callback): 
    global agreeaccaunt
    global isOpenEdit
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
    if isOpenEdit == True:

        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_lastname2(message) 
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, lastnameError)
                message.text.strip(None)
                input_lastname2(message) 
            else:
                lastname = message.text.strip()
                print(lastname)
                bot.edit_message_text('Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')

                input_firstname2(message)
    else:
        data(message)


def input_firstname2(message):
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
    if isOpenEdit == True:

        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_firstname2(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, firstnameError)
                message.text.strip(None)
                input_firstname2(message)        
            else:                  
                firstname = message.text.strip()    
                print(firstname_check)
                bot.edit_message_text('🖌Введи ТОЛЬКО имя как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')
                input_middlename2(message)
    else:
        data(message)

def input_middlename2(message):
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
    if isOpenEdit == True:
        if message.text is None:
            bot.send_message(message.from_user.id, textOnly)
            input_middlename2(message)
        else:
            if len(message.text.strip()) > maxSymbol:
                bot.send_message(message.chat.id, middlenameError)
                message.text.strip(None)
                input_middlename2(message) 
            else:     
                middlename = message.text.strip()
                print(middlename_check)
                bot.edit_message_text('🖌Введи ТОЛЬКО отчество как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')

                readyPassportInfo(message)
    else:
        data(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'Еду1')
def callback_data_of_data(callback): 
    if callback.data == 'Еду1':
        bot.send_message(callback.message.chat.id, 'Все работает', parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data == '❌ Отменить подтверждение')
def callback_delete_previos_message(callback): 
    global isOpenEdit
    if callback.data == '❌ Отменить подтверждение':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        isOpenEdit = False
        # data(callback.message)


def input_lastname(message):
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
    if isOpenEdit == True:
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
                bot.edit_message_text('Для подтверждения - отправь твои настоящие данные. Они не будут переданы третьим лицам.\n🖌Введи ТОЛЬКО фамилию как в паспорте:', message.chat.id, message.message_id - 1,  parse_mode='html')

                input_firstname(message)
    else:
        data(message)


def input_firstname(message):
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
    if isOpenEdit == True:

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
                bot.edit_message_text('🖌Введи ТОЛЬКО имя как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')

                input_middlename(message)
    else:
        data(message)

def input_middlename(message):
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
    if isOpenEdit == True:

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
                bot.edit_message_text('🖌Введи ТОЛЬКО отчество как в паспорте:', message.chat.id, message.message_id - 1, parse_mode='html')

                input_passport(message)
    else:
        data(message)

def input_passport(message):
    if isOpenEdit == True:

        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('❌ Отменить подтверждение', callback_data='❌ Отменить подтверждение', one_time_keyboard=True)
        markup.row(btn2)  
        bot.send_message(message.chat.id, 'ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, passport_check)
    else:
        data(message)

# @bot.message_handler(func=lambda message: bool(re.match(r'^\d{4} \d{6}$', message.text))) 
def passport_check(message):      
    global passport    
    # passport = message.text.strip()
    # print(passport)
    # readyPassportInfo(message)
    if isOpenEdit == True:

        if message.text is None:
            bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')

            bot.send_message(message.from_user.id, 'Введите цифры')

            input_passport(message)
        else:
            if len(message.text.strip()) != 10:
                bot.edit_message_text('ℹ️ Пользователи, полностью заполнившие данные, имеют приоритет при получении заявок.\n\nВведите Ваши серию и номер паспорта в формате XXXXYYYYYY, где XXXX - серия, YYYYYY - номер.', message.chat.id, message.message_id - 1, parse_mode='html')

                bot.send_message(message.chat.id, 'Введите цифры')
                message.text.strip(None)
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
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🖌Редактировать ФИО', callback_data='🖌Редактировать ФИО', one_time_keyboard=True)
    btn2 = types.InlineKeyboardButton('🖌Редактировать дату рождения',callback_data='🖌Редактировать ДР', one_time_keyboard=True)
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
    if callback.data == f'❌Удалить "{city}"':
        markup = types.InlineKeyboardMarkup()
        btn3 = types.InlineKeyboardButton('✅Добавить город', callback_data='✅Добавить город', one_time_keyboard=True) 
        markup.row(btn3)  
        bot.edit_message_text('Укажи город, где хочешь работать.', callback.message.chat.id, callback.message.message_id, reply_markup=markup)

    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)

@bot.callback_query_handler(func=lambda callback: callback.data == '✅Добавить город') 
def callback_add_city(callback):   
    if callback.data == '✅Добавить город':
        locationCityCitizen(callback.message)        

    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)


def locationCityCitizen(message):
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
    if callback.data == '✅Продолжить2':
        bot.answer_callback_query(callback_query_id=callback.id, text='Сначала нужно завершить редактирование данных. Чтобы завершить нажмите ✅Подтвердить',show_alert=True)
        data(callback.message)
    else:          
        bot.edit_message_text(f'Выбрано: 🟢{city}', callback.message.chat.id, callback.message.message_id)


if __name__ == '__main__':
    print('Bot started')
    bot.polling(non_stop=True)
