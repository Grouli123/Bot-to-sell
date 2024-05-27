import telebot
from telebot import types
import sqlite3
import time

botApiKey13 = '6489313384:AAFOdsE5ZTo1pdXL_JNl1lxF_QMRfZ9pE9A'
bot13 = telebot.TeleBot(botApiKey13)

def SendCloseMessage(chatcity, messageCard, user_id):
    print('itWork')
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        users = cur.fetchone() 
        if users:
            user_id_mess = users[0]
            print(user_id_mess)
        if chatcity != 'None':
            print("Заполненное значение botChatId:", chatcity)
            bot13.send_message(chatcity, f"{users[4]} {users[5]} {users[6]} завершил заказ, номер карты для перевода зп {messageCard}", parse_mode='html')
        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        print('Заказов пока нет, но скоро будут')
        conn.close()