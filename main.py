import random
from sqlite3 import Connection, Cursor

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from BotKey import botKey
import asyncio

api = botKey
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
# button_info: KeyboardButton = KeyboardButton('Информация')
# button_calc: KeyboardButton = KeyboardButton('Рассчитать')
# kb.add(button_info)
# kb.add(button_calc)

kb_inline = InlineKeyboardMarkup()
button_calc = InlineKeyboardButton(text='Рассчитать', callback_data='calc')
button_formula = InlineKeyboardButton(text='Формула для расчета калорий', callback_data='formula')
kb_inline.add(button_calc)
kb_inline.add(button_formula)


@dp.message_handler(commands=['start'])
async def star(message: Message):
    # print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_inline)


@dp.callback_query_handler(text='formula')
async def getFormula(call):

    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

# @dp.message_handler(text=['Информация'])
# async def star(message: Message):
#     await message.answer('Информация о боте')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calc')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state):
    await state.update_data(age=message.text)
    # data = await state.get_data()
    # print(data)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()
    # await state.finish()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state):
    await state.update_data(growth=message.text)
    # data = await state.get_data()
    # print(data)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # print(data)
    await message.answer(f'Ваша норма калорий: {10 * int(data["weight"]) + 6,25 * int(data["growth"]) - 5 * int(data["age"]) + 5}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':

    connection: Connection = sqlite3.connect('not_telegram.db')
    cursor: Cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    # cursor.execute('''
    # CREATE INDEX IF NOT EXISTS idx_email ON Users (email)
    # ''')

    # for i in range(30):
    #     cursor.execute(f'''
    #     INSERT INTO Users (username, email, age, balance) VALUES ("user{i}", "ex{i}.gmail.com", "{random.randint(18, 50)}", "{random.randint(100, 5000)}")
    #     ''')

    # cursor.execute('''
    # UPDATE Users SET balance = "500"
    # ''')

    # cursor.execute('''
    # DELETE FROM Users WHERE id % 3 = 0
    # ''')
    cursor.execute('''
    SELECT username, email, age, balance FROM Users WHERE age != 60
    ''')
    users = cursor.fetchall()

    for user in users:
        print(user)
        
    connection.commit()
    connection.close()
    # executor.start_polling(dp, skip_updates=True)

