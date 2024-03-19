import telebot
from telebot import types
import sqlite3
import time

botApiKey13 = '6433261921:AAEmTi8RVvhuSdYSlxB2uq0x3tP0X4wMRBE'
bot13 = telebot.TeleBot(botApiKey13)

def SendMessageintoHere(chatcity):
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
            bot13.send_message(chatcity, f"✅\nработает {users[2]}", parse_mode='html')

        cur.close()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        print('Заказов пока нет, но скоро будут')
        conn.close()

