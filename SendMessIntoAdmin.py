import telebot
from telebot import types
import sqlite3
import time

botApiKey13 = '6433261921:AAEmTi8RVvhuSdYSlxB2uq0x3tP0X4wMRBE'
bot13 = telebot.TeleBot(botApiKey13)

def SendMessageintoHere(chatcity, user_id):
    print('itWork')
    
    # Initialize database connection
    conn = sqlite3.connect('custumers.sql', check_same_thread=False)
    cur = conn.cursor()
    
    try:
        # Create table if it doesn't exist
        # cur.execute('''CREATE TABLE IF NOT EXISTS custumers
        #                (id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 user_id INTEGER,
        #                 phone TEXT,
        #                 lastname TEXT,
        #                 firstname TEXT,
        #                 middlename TEXT)''')
        
        # Query the database
        cur.execute("SELECT * FROM custumers WHERE user_id = ?", (user_id,))
        users = cur.fetchone()

        if users:
            user_id_mess = users[0]
            print(f"User ID found: {user_id_mess}")
            print(f"Phone: {users[2]}")
            print(f"Lastname: {users[3]}")
            print(f"Firstname: {users[4]}")
            print(f"Middlename: {users[5]}")

            if chatcity != 'None':
                bot13.send_message(chatcity, f"✅\nПользователь {users[3]} {users[4]} {users[5]} с номером телефона {users[2]} зарегистрировался, в качестве заказчика", parse_mode='html')
        else:
            print('User not found in the database')

        conn.commit()
        conn.close()
        time.sleep(3)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        print(f"Database connection details: {conn}")
        print(f"Cursor details: {cur}")
        conn.close()
    finally:
        if conn:
            conn.close()
