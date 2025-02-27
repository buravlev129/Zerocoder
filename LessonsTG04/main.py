import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config import TOKEN
from keyboards import kbd_reply_markup, inline_keyboard, create_salad_keyboard, create_vegetable_keyboard, get_vegetable_name


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("help"))
async def help(message: Message):
    bf = """
    Команды:
    /start    - Запустить бота
    /links    - Ссылки на рецепты
    /dynamic  - Динамические кнопки
    /help     - Получить справку по командам
    """
    await message.answer(bf)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Тестовый бот с кнопками", reply_markup=kbd_reply_markup)


@dp.message(F.text == "Привет 👋")
async def hello(message: Message):
    username = message.from_user.username
    await message.answer(f"Привет, {username}!")

@dp.message(F.text == "Пока ✋🏼")
async def Goodby(message: Message):
    username = message.from_user.username
    await message.answer(f"До свидания, {username}!")


@dp.message(Command("links"))
async def get_links(message: Message):
    await message.answer("URL-ссылки", reply_markup=inline_keyboard)


@dp.message(Command("dynamic"))
async def get_dynamic(message: Message):
    await message.answer("Выберите овощ", reply_markup=create_vegetable_keyboard())


@dp.callback_query(lambda query: query.data.startswith("vegetable:"))
async def show_salads(query: CallbackQuery):
    key = query.data.split(":")[1]
    name = get_vegetable_name(key)
    await query.message.edit_text(f"Салаты из {name}:", reply_markup=create_salad_keyboard(key))


@dp.callback_query(lambda query: query.data == "back_to_menu")
async def back_to_menu(query: CallbackQuery):
    await query.message.edit_text("Выберите овощ:", reply_markup=create_vegetable_keyboard())


@dp.callback_query(lambda query: query.data.startswith("salad:"))
async def show_salad_info(query: CallbackQuery):
    salad = query.data.split(":")[1]
    await query.answer(f"Вы выбрали: {salad}", show_alert=True)



@dp.message(Command("help"))
async def help(message: Message):
    bf = """
    Команды:
    /start    - Запустить бота
    /links    - URL-ссылки
    /dynamic  - Динамическая клавиатура
    /help     - Справка по командам
    """
    await message.answer(bf)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
