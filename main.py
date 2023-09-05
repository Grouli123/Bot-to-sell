import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6484701618:AAFcxH0T31Rl_XakKMfFm5PWsLwSIRzhcVE')

currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Впишите сумму")
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Введите пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0. Впишите сумму")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значение через слэш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите значение заново')
        bot.register_next_step_handler(message, my_currency)








# Погода
# api_key = 'e94d9b9ab618e8073f97fe7def3443b3'

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'Привет, напиши название города')

# @bot.message_handler(content_types=['text'])
# def get_weather(message):
#     city = message.text.strip().lower()
#     res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
#     if res.status_code == 200:
#         data = json.loads(res.text)
#         temp = data["main"]["temp"] 
#         bot.reply_to(message, f'Сейчас погода: {temp}')

#         image = 'sunny.png' if temp > 5.0 else 'sun.png'
#         file = open('./' + image, 'rb')
#         bot.send_photo(message.chat.id, file)
#     else:
#         bot.reply_to(message, 'Город указан не верно')















# SQL base

name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите ваше имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('peoplebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)





# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup()
#     btn1 = types.KeyboardButton('Перейти на сайт')
#     btn2 = types.KeyboardButton('Удалить фото')
#     btn3 = types.KeyboardButton('Изменить текст')
#     markup.row(btn1)
#     markup.row(btn2, btn3)    
#     # file = open('./Wckf4VbNRX8.jpg', 'rb')
#     # bot.send_photo(message.chat.id, file, reply_markup=markup)    
#     bot.send_message(message.chat.id, 'Привет',  reply_markup=markup)
#     bot.register_next_step_handler(message, on_click)

# def on_click(message):
#     if message.text == 'Перейти на сайт':
#         bot.send_message(message.chat.id, "website is open")
#     elif message.text == 'Удалить фото':
#         bot.send_message(message.chat.id, "delete")


# нажатие на кнопку сайт
@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://google.com')

# нажатие на кнопку start
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}' )

# нажатие на кнопку help
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Помощь</b> <em><u>бота</u></em>',parse_mode='html')

# работа с фото
@bot.message_handler(content_types=['text'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    btn2 = types.InlineKeyboardButton('Удалить текст', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст на edit', callback_data='edit')
    markup.row(btn1)
    markup.row(btn2, btn3)    
    bot.reply_to(message, "Я тут", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

# ответ на привет или id
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}' )
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    
bot.polling(non_stop=True)





# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):        
#     if callback.data == 'Да':
#         bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: Есть')
#     elif callback.data == 'Нет':
#         bot.send_message(callback.message.chat.id, f'📞 Телефон: {phone}\n👤 ФИО: {lastname} {firstname} {middlename}\n📅 Дата рождения: {userbirthday}\n🇷🇺 Гражданство РФ: Нет')
