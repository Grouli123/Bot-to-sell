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
orderTakeTwo = ''


fioFirstFriend = None
fioSecondFriend = None
fioThirdFriend = None


phoneNumberFirstFriend = None
phoneNumberSecondFriend = None
phoneNumberThirdFriend = None

checkThirdFriend = False
checkFourthFriend = False

# messageChatId = '1098274481'
messageChatId = None

global_user_id = None

test = None


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

    global messageChatId

    data_called = False

    messageChatId = message.chat.id

    print(messageChatId)
    
    user_id = message.from_user.id

    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
          # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone() # Получение первой соответствующей строки

    

    if takeParam:
        check_user_id = takeParam[9]

    else:
        check_user_id = None

    cursor.execute("UPDATE users SET botChatId = ('%s') WHERE user_id = ('%s')" % (messageChatId, user_id))
    conn.commit()
    cursor.close()
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

    print('А тут?', messageChatId)
    try:
        cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
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
            
                
            order_info = f'✅\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n<b>•Адрес:</b>👉 {users[4]}\n<b>•Что делать:</b> {users[5]}\n<b>•Начало работ:</b> в {users[6]}\n<b>•Вам на руки:</b> <u>{users[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'
                
                
            if order_info != last_sent_message:
                    
                print('работает елсе')

                # Получаем ID пользователя
                user_id_mess = users[0]
                print(user_id_mess)
                # Получаем текущий список message_id из базы данных
                cur.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % (user_id_mess))
                current_message_ids_str = cur.fetchone()[0]
                    
                # Преобразуем текущую строку в список (если она не пуста)
                current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []
                
                for result in results:
                    botChatIdw = result[0]  # Получаем значение botChatId из результата
                    if botChatIdw != 'None':
                        print("Заполненное значение botChatId:", botChatIdw)

                        sent_message = bot.send_message(botChatIdw, order_info, reply_markup=markup2, parse_mode='html')
                        last_message_id = sent_message.message_id  


                        user_chat_id_str = user_chat_ids.get(user_id_mess, "")
                        if user_chat_id_str:
                            user_chat_id_str += ","
                        user_chat_id_str += str(botChatIdw)
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
                cur5.close()
                conn5.close()   

                    

                
                for user_id_mess, message_id_list in user_message_ids.items():
                    updated_message_ids_str = ','.join(map(str, message_id_list))
                    sql_query = "UPDATE orders SET orderMessageId = ('%s'), orderChatId = ('%s') WHERE id = ('%s')"
                    cur.execute(sql_query % (updated_message_ids_str, user_chat_id_str, user_id_mess))

                # Коммит изменений в базу данных
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
        # Обработка ошибки, если таблицы нет или произошла другая ошибка
        if not error_reported:
                
            print('Заказов пока нет, но скоро будут')
            error_reported = True  # Устанавливаем флаг ошибки, чтобы сообщение выводилось только один раз
    
        # Закрытие соединения с базой данных
        conn.close()
    
@bot.callback_query_handler(func=lambda callback: callback.data == 'Еду 1')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 2') 
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 3')
@bot.callback_query_handler(func=lambda callback: callback.data == 'Едем в 4')
def callback_data_of_data(callback): 
    global orderTakeTwo
    global checkThirdFriend
    global checkFourthFriend
    global user_id_mess
    global test
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam2 = cursor.fetchone() # Получение первой соответствующей строки
    print('юзер айди ',user_id_mess)
    if takeParam2[9] != '':
        if takeParam2:
            orderTakeTwo = takeParam2[0]
            print(orderTakeTwo)
            print('работает')
        else:
            print('не работает')

        if callback.data == 'Еду 1':
            test = callback.message.message_id

            cursor.execute("SELECT orderTake FROM users WHERE user_id = ('%s')" % (user_id))
            takeOrderTake = cursor.fetchone()

            
            if takeOrderTake is not None:
                current_orderId = takeOrderTake[0] if takeOrderTake[0] else ""


                conn3 = sqlite3.connect('applicationbase.sql')
                cur3 = conn3.cursor()
                cur3.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
                users = cur3.fetchone() 
                print(callback.message.message_id)
                
                # Получаем ID пользователя
                user_id_mess = users[0]
                
                cur3.close()
                conn3.close()

                new_orderId = current_orderId + "," + str(user_id_mess) if current_orderId else user_id_mess
                cursor.execute("UPDATE users SET orderTake = '%s' WHERE user_id = '%s'" % (new_orderId, user_id))
                
                

            conn.commit()
            cursor.close()
            conn.close()

            conn2 = sqlite3.connect('applicationbase.sql')
            cursor2 = conn2.cursor()        

            cursor2.execute("SELECT whoTakeId FROM orders WHERE orderMessageId = ('%s')" % (test))
            current_values = cursor2.fetchone()
            print('карент пхон ', current_values)
            if current_values is not None:
                current_phone_numbers = current_values[0] if current_values[0] else ""
                print(type(current_phone_numbers))
                print('nen ', current_phone_numbers)
                
                print('Тут ', orderTakeTwo)
                

                new_phone_numbers = current_phone_numbers + "," + str(orderTakeTwo) if current_phone_numbers else orderTakeTwo

                print('нею пхоне', new_phone_numbers)

                cursor2.execute("UPDATE orders SET whoTakeId = '%s' WHERE orderMessageId = '%s'" % (new_phone_numbers, test))
                print(cursor2)
                conn2.commit()

            else:  
                print('тут не работает')

            cursor2.close()
            conn2.close()

        
            conn2 = sqlite3.connect('applicationbase.sql')
            cursor2 = conn2.cursor()        


            



            cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
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

            order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

            bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

            bot.send_message(callback.message.chat.id, f'Принято, вы едете 1, ваш заказ номер: {user_id_mess}\n записался на заказ номер: {orderTakeTwo}') 
            conn2.commit()
            cursor2.close()
            conn2.close()
        elif callback.data == 'Едем в 2':
            test = callback.message.message_id

            conn3 = sqlite3.connect('applicationbase.sql')
            cur3 = conn3.cursor()
            cur3.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
            users = cur3.fetchone() 
            print(callback.message.message_id)
                
                # Получаем ID пользователя
            user_id_mess = users[0]
                
            cur3.close()
            conn3.close()

            conn2 = sqlite3.connect('applicationbase.sql')
            cursor2 = conn2.cursor()        

            cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
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

            order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

            bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

            conn2.commit()
            cursor2.close()
            conn2.close()
            input_fio_first_friend(callback.message)

        elif callback.data == 'Едем в 3':
            test = callback.message.message_id

            
            conn3 = sqlite3.connect('applicationbase.sql')
            cur3 = conn3.cursor()
            cur3.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
            users = cur3.fetchone() 
            print(callback.message.message_id)
                
                # Получаем ID пользователя
            user_id_mess = users[0]
                
            cur3.close()
            conn3.close()

            checkThirdFriend = True
            conn2 = sqlite3.connect('applicationbase.sql')
            cursor2 = conn2.cursor()        

            cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
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

            order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

            bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

            conn2.commit()
            cursor2.close()
            conn2.close()
            input_fio_first_friend(callback.message)
        elif callback.data == 'Едем в 4': 
            test = callback.message.message_id

            
            conn3 = sqlite3.connect('applicationbase.sql')
            cur3 = conn3.cursor()
            cur3.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
            users = cur3.fetchone() 
            print(callback.message.message_id)
                
                # Получаем ID пользователя
            user_id_mess = users[0]
                
            cur3.close()
            conn3.close()
            
            checkThirdFriend = True
            checkFourthFriend = True       
            conn2 = sqlite3.connect('applicationbase.sql')
            cursor2 = conn2.cursor()        

            cursor2.execute("SELECT * FROM orders WHERE orderMessageId = ('%s')" % (test))
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

            order_info = f'✅\n<b>•{table_element[2]}: </b>{needText} {table_element[3]} {humanCount}\n<b>•Адрес:</b>👉 {table_element[4]}\n<b>•Что делать:</b> {table_element[5]}\n<b>•Начало работ:</b> в {table_element[6]}\n<b>•Вам на руки:</b> <u>{table_element[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

            bot.edit_message_text(order_info, callback.message.chat.id, callback.message.message_id, parse_mode='html')

            conn2.commit()
            cursor2.close()
            conn2.close()
            input_fio_first_friend(callback.message)
    else:
        markup1 = types.InlineKeyboardMarkup()
        btn01 = types.InlineKeyboardButton('✅ Зарегистрироваться', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup1.row(btn01)
        bot.send_message(callback.message.chat.id, 'Для того чтобы записаться на заказ, вы должны быть зарегистрированы', parse_mode='html', reply_markup= markup1)


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


                    cursor2.execute("SELECT whoTakeId FROM orders WHERE orderMessageId = ('%s')" % (test))
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

                cursor2.execute("SELECT whoTakeId FROM orders WHERE orderMessageId = ('%s')" % (test))
                current_values = cursor2.fetchone()
                print(user_id_mess)
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
                
                bot.send_message(message.chat.id, f'Вы {famname} {actualName} {otchName} номер телефона: {userPhone}.\nВаши друзья:\n1.{fioFirstFriend} номер телефона: {phoneNumberFirstFriend}\n2. {fioSecondFriend} номер телефона: {phoneNumberSecondFriend}\n 3. {fioThirdFriend} номер телефона: {phoneNumberThirdFriend}', parse_mode='html')

                

                print('Номер телефона друга: ', phoneNumberFirstFriend, 'ФИО друга: ', fioFirstFriend)
                print('Номер телефона друга: ', phoneNumberSecondFriend, 'ФИО друга: ', fioSecondFriend)
                print('Номер телефона друга: ', phoneNumberThirdFriend, 'ФИО друга: ', fioThirdFriend)
            else:
                bot.send_message(message.chat.id, 'Введите корректный номер телефона друга без "+" и без пробелов, который начинается с 7 или с 8:', parse_mode='html')
                input_third_friend_number(message)







if __name__ == '__main__':
    print('Bot started')
    bot.polling(non_stop=True)
