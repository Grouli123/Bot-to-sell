from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('6484701618:AAFcxH0T31Rl_XakKMfFm5PWsLwSIRzhcVE')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://Google.com')))
    await message.answer('Привет, мой друг!', reply_markup=markup)


















# @dp.message_handler(content_types=['photo']) #commands=['start']
# async def start(message: types.Message):
#     # await bot.send_message(message.chat.id, 'Hello')
#     # await message.answer('Hello')
#     await message.reply('Hello')
#     # file = open('./Wckf4VbNRX8.jpg', 'rb')
#     # await message.answer_photo(file)

# @dp.message_handler(commands=['inline'])
# async def info(message: types.Message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     markup.add(types.InlineKeyboardButton('site', url='https://google.com'))
#     markup.add(types.InlineKeyboardButton('Hello', callback_data='Hello'))
#     await message.reply('Hello', reply_markup=markup)


# @dp.callback_query_handler()
# async def callback(call):
#     await call.message.answer(call.data)

# @dp.message_handler(commands=['reply'])
# async def reply(message: types.Message):
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#     markup.add(types.KeyboardButton('Site'))
#     markup.add(types.KeyboardButton('WebSite'))
#     await message.answer('hello', reply_markup=markup)



executor.start_polling(dp)