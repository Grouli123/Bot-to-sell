from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3

import  get_orders_config.get_orders_API_key as API_key
import  get_orders_config.get_orders_config_message as config_message

import time

botApiKey = API_key.botAPIArz


bot = Bot(botApiKey)
dp = Dispatcher(bot)



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




# Определение функции для мониторинга базы данных
# def database_monitor():
#     while True:
#         conn = sqlite3.connect('applicationbase.sql')
#         cur = conn.cursor()

#         try:
#             cur.execute('SELECT * FROM orders ORDER BY id DESC LIMIT 1')
#             users = cur.fetchone()

#             if users is not None:
#                 # Ваш код мониторинга базы данных
#                 # ...
#             else:
#                 print('Заказов пока нет, но скоро будут')

#         except sqlite3.Error as e:
#             # Обработка ошибки
#             pass

#         cur.close()
#         conn.close()
#         time.sleep(3)
@dp.message_handler(commands=['start'])
async def registration(message: types.Message):
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
    global user_id_mess

    data_called = False

    user_id = message.from_user.id
    conn = sqlite3.connect('peoplebase.sql')
    cursor = conn.cursor()
    # Запрос к базе данных для поиска строки по значению переменной
    cursor.execute("SELECT * FROM users WHERE user_id = ('%s')" % (user_id))
    takeParam = cursor.fetchone()  # Получение первой соответствующей строки

    if takeParam:
        check_user_id = takeParam[9]
    else:
        check_user_id = None
    conn.close()

    if check_user_id is not None or user_id is not None:
        await message.answer(f'Поздравляем с успешной регистрацией✅\nОжидай появления новых заявок!\nПринять заявку можно, нажав на активные кнопки под заявкой.\n\nℹ️Если хочешь видеть все заявки и иметь преимущество в назначении на заявку - подтверди свой аккаунт (это можно сделать в любой момент). Для этого нажми на кнопку "👤Мои данные" на твоей клавиатуре внизу, затем нажми "✅Подтвердить аккаунт"👇👇👇', parse_mode='html')
        userCitizenRuText = f'👉Пока можешь почитать отзывы о нашей организации'
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton(citizenRuButtonYesText, callback_data=citizenRuButtonYesTextCallbackData, one_time_keyboard=True)
        btn3 = types.InlineKeyboardButton(citizenRuButtonNoText, callback_data=citizenRuButtonNoTextCallbackData, one_time_keyboard=True)
        markup.row(btn2)
        markup.row(btn3)
        await message.answer(userCitizenRuText, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('👉 Перейти к боту регистрации', url='https://t.me/GraeYeBot', one_time_keyboard=True)
        markup.row(btn2)
        await message.answer(f'Для регистрации перейдите к боту по кнопке!\n\n👇👇👇👇👇', parse_mode='html', reply_markup=markup)

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

                order_info = f'✅\n<b>•{users[2]}: </b>{needText} {users[3]} {humanCount}\n<b>•Адрес:</b>👉 {users[4]}\n<b>•Что делать:</b> {users[5]}\n<b>•Начало работ:</b> в {users[6]}\n<b>•Вам на руки:</b> <u>{users[7]}.00</u> р./час, минималка 2 часа\n<b>•Приоритет самозанятым</b>'

                if order_info != last_sent_message:
                    conn = sqlite3.connect('applicationbase.sql')
                    cursor = conn.cursor()

                    # Получаем ID пользователя
                    user_id_mess = users[0]
                    # Получаем текущий список message_id из базы данных
                    cursor.execute("SELECT orderMessageId FROM orders WHERE id = ('%s')" % (user_id_mess))
                    current_message_ids_str = cursor.fetchone()[0]

                    # Преобразуем текущую строку в список (если она не пуста)
                    current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []

                    messageChatId = message.chat.id
                    sent_message = await bot.send_message(messageChatId, order_info, reply_markup=markup2, parse_mode='html')
                    last_message_id = sent_message.message_id

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

                    for user_id_mess, message_id_list in user_message_ids.items():
                        updated_message_ids_str = ','.join(map(str, message_id_list))
                        sql_query = "UPDATE orders SET orderMessageId = ('%s'), orderChatId = ('%s') WHERE id = ('%s')"
                        cursor.execute(sql_query % (updated_message_ids_str, user_chat_id_str, user_id_mess))

                    # Коммит изменений в базу данных
                    conn.commit()
                    last_sent_message = order_info
                    check_mess_already_send = False
                else:
                    print('Нет новых сообщений')
            
            cur.close()
            conn.close()
            time.sleep(3)
        except sqlite3.Error as e:
            # Обработка ошибки, если таблицы нет или произошла другая ошибка
            if not error_reported:
                print('Заказов пока нет, но скоро будут')
                error_reported = True  # Устанавливаем флаг ошибки, чтобы сообщение выводилось только один раз

        conn.close()

if __name__ == '__main__':
    print('Bot started')

    executor.start_polling(dp, skip_updates=True)
