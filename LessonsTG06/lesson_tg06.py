import asyncio
import sqlite3
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import TOKEN, EXCHANGE_RATE_KEY
from keyboards import kbd_reply_markup
from econimitips import get_random_tip


bot = Bot(token=TOKEN)
dp = Dispatcher()


conn = sqlite3.connect("user.db")
cursor = conn.execute("""
create table if not exists users (
    id integer primary key,
    telegram_id integer unique,                  
    name text,
    category1 text,
    category2 text,
    category3 text,
    expenses1 real,
    expenses2 real,
    expenses3 real
    )
""")

conn.commit()


class FinanceForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()



@dp.message(CommandStart())
async def start(message: Message):
    bf = "Привет! Я финансовый бот помощник. Выберите одну из опций в меню"
    await message.answer(bf, reply_markup=kbd_reply_markup)


@dp.message(F.text=="Регистрация")
async def registration(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    telegram_id = message.from_user.id
    name = message.from_user.full_name

    cursor.execute("""select * from users where telegram_id = ?""", (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer("Вы уже зарегистрированы")
    else:
        cursor.execute("""insert into users (telegram_id, name) values (?, ?)""", (telegram_id, name))
        conn.commit()
        await message.answer("Вы успешно зарегистрированы")


@dp.message(F.text=="Курс валют")
async def get_exchange_rates(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_KEY}/latest/USD"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            await message.answer("Не удалось получить данные по курсам валют")
            return

        data = response.json()
        usd_to_rub = data["conversion_rates"]["RUB"]
        eur_to_usd = data["conversion_rates"]["EUR"]
        eur_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f"1 USD: {usd_to_rub:.2f} RUB\n"
                             f"1 EUR: {eur_to_rub:.2f} RUB")

    except Exception as ex:
        await message.answer(f"ОШИБКА: {str(ex)}")


@dp.message(F.text=="Советы по экономии")
async def send_tips(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    tip = get_random_tip()
    await message.answer(tip)


@dp.message(F.text=="Личные финансы")
async def finances_с1(message: Message, state: FSMContext):
    await state.set_state(FinanceForm.category1)
    await message.reply("Введите первую категорию расходов:")


@dp.message(FinanceForm.category1)
async def finances_ex1(message: Message, state: FSMContext):
    await state.update_data(category1 = message.text)
    await state.set_state(FinanceForm.expenses1)
    await message.reply("Введите расходы для категории 1:")


@dp.message(FinanceForm.expenses1)
async def finances_с2(message: Message, state: FSMContext):
    await state.update_data(expenses1 = float(message.text))
    await state.set_state(FinanceForm.category2)
    await message.reply("Введите вторую категорию расходов:")


@dp.message(FinanceForm.category2)
async def finances_ex2(message: Message, state: FSMContext):
    await state.update_data(category2 = message.text)
    await state.set_state(FinanceForm.expenses2)
    await message.reply("Введите расходы для категории 2:")


@dp.message(FinanceForm.expenses2)
async def finances_c3(message: Message, state: FSMContext):
    await state.update_data(expenses2 = float(message.text))
    await state.set_state(FinanceForm.category3)
    await message.reply("Введите третью категорию расходов:")


@dp.message(FinanceForm.category3)
async def finances_ex3(message: Message, state: FSMContext):
    await state.update_data(category3 = message.text)
    await state.set_state(FinanceForm.expenses3)
    await message.reply("Введите расходы для категории 3:")


@dp.message(FinanceForm.expenses3)
async def finances_c3(message: Message, state: FSMContext):
    expenses3 = float(message.text)

    dt = await state.get_data()
    telegram_id = message.from_user.id

    bf = """update users set category1=?, expenses1=?, category2=?, expenses2=?, category3=?, expenses3=? where telegram_id=?"""
    cursor.execute(bf, (dt["category1"], dt["expenses1"], dt["category2"], dt["expenses2"], dt["category3"], expenses3, telegram_id) )
    conn.commit()

    await state.clear()
    await message.reply("Категории и расходы сохранены")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
