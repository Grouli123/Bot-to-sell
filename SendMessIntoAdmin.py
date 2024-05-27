import telebot
from telebot import types
import sqlite3
import time

botApiKey13 = '6433261921:AAEmTi8RVvhuSdYSlxB2uq0x3tP0X4wMRBE'
bot13 = telebot.TeleBot(botApiKey13)

def SendMessageintoHere(chatcity, user_id):
    print('itWork')
    conn = sqlite3.connect('custumers.sql')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM custumers WHERE user_id = ?", (user_id,))
        users = cur.fetchone() 

        if users:
            user_id_mess = users[0]
            print(user_id_mess)
        if chatcity != 'None':
            print("Заполненное значение botChatId:", chatcity)
            bot13.send_message(chatcity, f"✅\nПользователь {users[4]} {users[5]} {users[6]}  с номером телефона {users[2]} зарегистрировался, в качестве заказчика", parse_mode='html')
        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        print('Заказов пока нет, но скоро будут')
        conn.close()