import telebot
from telebot import types
import sqlite3
import time  # Не забудьте импортировать time
from datetime import datetime, timedelta  # Если используются в другом коде

check_mess_already_send = False
check_user_id = None
last_sent_message = None
humanCount = None
needText = None
last_message_id = None  
error_reported = False  # Флаг для отслеживания, была ли ошибка уже выведена
user_last_message_ids = {}
user_message_ids = {}
user_chat_ids = {}
data_called = False  
user_id_mess = None

callbackGetData= None

def testMethod(botId):
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

    bot = telebot.TeleBot(botId)

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
        if users is not None and users[2]:
            if (int(users[3]) <= 1) or (int(users[3]) >= 5):
                humanCount = 'человек'
            else:
                humanCount = 'человека'
            if int(users[3]) > 1:
                needText = 'Нужно'
            else:
                needText = 'Нужен'

            # Получаем идентификатор заказа
            order_id = users[0]

            # Создаем кнопки с включением order_id в callback_data
            markup2 = types.InlineKeyboardMarkup()
            if int(users[3]) == 1:
                callbackGetData = f'Еду 1|{order_id}'
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data=callbackGetData, one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn52)
            elif int(users[3]) == 2:
                callbackGetData1 = f'Еду 1|{order_id}'
                callbackGetData2 = f'Едем в 2|{order_id}'
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data=callbackGetData1, one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data=callbackGetData2, one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn22)
                markup2.row(btn52)
            elif int(users[3]) == 3:
                callbackGetData1 = f'Еду 1|{order_id}'
                callbackGetData2 = f'Едем в 2|{order_id}'
                callbackGetData3 = f'Едем в 3|{order_id}'
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data=callbackGetData1, one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data=callbackGetData2, one_time_keyboard=True)
                btn32 = types.InlineKeyboardButton('Едем в 3', callback_data=callbackGetData3, one_time_keyboard=True)
                btn52 = types.InlineKeyboardButton('❓ Задать вопрос', url='https://t.me/Grouli123', one_time_keyboard=True)
                markup2.row(btn12)
                markup2.row(btn22)
                markup2.row(btn32)
                markup2.row(btn52)
            elif int(users[3]) >= 4:
                callbackGetData1 = f'Еду 1|{order_id}'
                callbackGetData2 = f'Едем в 2|{order_id}'
                callbackGetData3 = f'Едем в 3|{order_id}'
                callbackGetData4 = f'Едем в 4|{order_id}'
                btn12 = types.InlineKeyboardButton('Еду 1', callback_data=callbackGetData1, one_time_keyboard=True)
                btn22 = types.InlineKeyboardButton('Едем в 2', callback_data=callbackGetData2, one_time_keyboard=True)
                btn32 = types.InlineKeyboardButton('Едем в 3', callback_data=callbackGetData3, one_time_keyboard=True)
                btn42 = types.InlineKeyboardButton('Едем в 4', callback_data=callbackGetData4, one_time_keyboard=True)
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
                          f'<b>•Рабочее время:</b> {users[17]}:00\n'
                          f'<b>•Вам на руки:</b> <u>{users[8]}.00</u> р./час, минималка 2 часа\n'
                          f'<b>•Приоритет самозанятым</b>')

            if order_info != last_sent_message:
                user_id_mess = users[0]
                cur.execute("SELECT orderMessageId FROM orders WHERE id = ?", (user_id_mess,))
                current_message_ids_str = cur.fetchone()[0]
                current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []

                # Проходим по всем пользователям и отправляем сообщение 1 раз в каждый чат
                for result in results:
                    botChatIdw = result[0]
                    if botChatIdw != 'None':
                        try:
                            if str(botChatIdw) not in user_chat_ids.get(user_id_mess, "").split(","):
                                sent_message = bot.send_message(botChatIdw, order_info, reply_markup=markup2, parse_mode='html')
                                last_message_id = sent_message.message_id

                                # Обновляем данные отправленных сообщений для каждого чата
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

                        except telebot.apihelper.ApiException as e:
                            if "chat not found" in str(e):
                                print(f"Чат {botChatIdw} не найден, пропускаем отправку.")
                            else:
                                print(f"Ошибка при отправке сообщения в чат {botChatIdw}: {e}")

                # Теперь мы закрываем только после выполнения всех операций
                cur5.close()
                conn5.close()

                # Обновляем данные для всех пользователей
                for user_id_mess, message_id_list in user_message_ids.items():
                    updated_message_ids_str = ','.join(map(str, message_id_list))
                    print(f'updated_message_ids_str {updated_message_ids_str}')
                    print(f'user_chat_ids[user_id_mess] {user_chat_ids[user_id_mess]}')
                    sql_query = "UPDATE orders SET orderMessageId = ?, orderChatId = ? WHERE id = ?"
                    cur.execute(sql_query, (updated_message_ids_str, user_chat_ids[user_id_mess], user_id_mess))
                
                # Сохраняем изменения в базе данных после всех обновлений
                conn.commit()

                # Обновляем состояние сообщений
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
            print(f"Ошибка базы данных: {e}")
            error_reported = True
        conn.close()

