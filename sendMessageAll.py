import telebot
from telebot import types
import sqlite3
import time

# Глобальные переменные
check_mess_already_send = False
check_user_id = None
last_sent_message = None
error_reported = False
user_message_ids = {}
user_chat_ids = {}
last_message_id = None
user_id_mess = None

def sendNotyfiMessage(botId):
    global last_sent_message
    global error_reported
    global user_message_ids
    global user_chat_ids
    global last_message_id
    global user_id_mess

    bot = telebot.TeleBot(botId)

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

            if order_info != last_sent_message:
                user_id_mess = users[0]
                cur.execute("SELECT orderMessageId FROM orders WHERE id = ?", (user_id_mess,))
                current_message_ids_str = cur.fetchone()[0]
                current_message_ids = current_message_ids_str.split(',') if current_message_ids_str else []

                for result in results:
                    botChatIdw = result[0]
                    if botChatIdw != 'None':
                        if botChatIdw not in user_chat_ids.get(user_id_mess, "").split(","):
                            # Отправляем сообщение только в чаты, где оно еще не было отправлено
                            sent_message = bot.send_message(botChatIdw, order_info, parse_mode='html')
                            last_message_id = sent_message.message_id

                            # Обновляем информацию о чате и сообщениях
                            user_chat_id_str = user_chat_ids.get(user_id_mess, "")
                            if user_chat_id_str:
                                user_chat_id_str += ","
                            user_chat_id_str += str(botChatIdw)
                            user_chat_ids[user_id_mess] = user_chat_id_str

                            user_message_id_list = user_message_ids.get(user_id_mess, [])
                            user_message_id_list.append(last_message_id)
                            user_message_ids[user_id_mess] = user_message_id_list

                            current_message_ids.append(str(last_message_id))

                cur5.close()
                conn5.close()

                # Обновляем базу данных после отправки сообщений
                for user_id_mess, message_id_list in user_message_ids.items():
                    updated_message_ids_str = ','.join(map(str, message_id_list))
                    sql_query = "UPDATE orders SET orderMessageId = ?, orderChatId = ? WHERE id = ?"
                    cur.execute(sql_query, (updated_message_ids_str, user_chat_ids[user_id_mess], user_id_mess))

                conn.commit()
                last_sent_message = order_info
            else:
                print('Нет новых сообщений')

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
