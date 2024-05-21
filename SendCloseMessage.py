import telebot
from telebot import types
import sqlite3
import time

botApiKey13 = '6489313384:AAFOdsE5ZTo1pdXL_JNl1lxF_QMRfZ9pE9A'
bot13 = telebot.TeleBot(botApiKey13)

def SendCloseMessage(chatcity):
    print('itWork')
    conn = sqlite3.connect('custumers.sql')
    cur = conn.cursor()

    try:
        # Fetch the last customer's ID, but we don't use it here
        cur.execute("SELECT * FROM custumers ORDER BY id DESC LIMIT 1")
        users = cur.fetchone() 

        if users:
            user_id_mess = users[0]
            print(user_id_mess)

        # Directly use chatcity to send the message, without iterating over phone numbers
        if chatcity != 'None':
            print("Заполненное значение botChatId:", chatcity)
            bot13.send_message(chatcity, f"{users[4]} {users[5]} {users[6]} завершил заказ", parse_mode='html')

        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        print('Заказов пока нет, но скоро будут')
        conn.close()


