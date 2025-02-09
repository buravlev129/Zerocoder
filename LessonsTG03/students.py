import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from tabulate import tabulate

from config import TOKEN


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


database_name = "school_data.db"

def init_db():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("""
    create table if not exists students (
        id integer primary key autoincrement ,
        name text not null ,
        age integer not null ,
        grade text not null
        )
    """)
    conn.commit()
    conn.close()


init_db()


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f"Привет, как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    student = await state.get_data()
    await message.answer(f"Сколько тебе лет, {student["name"]}?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def form_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    student = await state.get_data()
    await message.answer(f"{student["name"]}, в каком классе ты учишься?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def form_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)

    student = await state.get_data()
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("insert into students (name, age, grade) values (?, ?, ?)", (student["name"], student["age"], student["grade"]))
    conn.commit()
    conn.close()

    await state.clear()



@dp.message(Command("help"))
async def help(message: Message):
    bf = """
    Команды:
    /help     - Справка по командам
    /start    - Запуск бота
     *Ввод данных*
      - Имя
      - Возраст
      - Класс
     *Получение данных*
    /get      - Получить список студентов
    """
    await message.answer(bf, parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("get"))
async def get_students(message: Message):

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    table = tabulate(rows, headers=["ID", "Имя", "Возраст", "Группа"], tablefmt="pretty")
    conn.close()

    await bot.send_message(message.chat.id, text=f"<pre>{table}</pre>", parse_mode="HTML")




@dp.message()
async def any_message(message: Message):
    await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
