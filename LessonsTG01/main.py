import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, OPENWEATHERMAP_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот для поиска информации о погоде")


@dp.message(Command("help"))
async def help(message: Message):
    bf = """
    Команды:
    /start    - Запустить бота
    /help     - Получить справку по командам
    Информация о погоде:
     - Просто укажите название города
    """
    await message.answer(bf)


@dp.message()
async def get_weather(message: Message):
    city = message.text
    weather_data = await fetch_weather(city)
    
    if weather_data:
        response = format_weather_response(weather_data)
    else:
        response = "Не удалось получить данные о погоде. Проверьте название города и попробуйте снова."
    
    await message.reply(response, parse_mode=ParseMode.MARKDOWN)


async def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None


def format_weather_response(weather_data):
    city = weather_data['name']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    description = weather_data['weather'][0]['description']
    
    return (f"🌍 *Город:* {city}\n"
            f"🌡️ *Температура:* {temperature}°C\n"
            f"💧 *Влажность:* {humidity}%\n"
            f"🌬️ *Скорость ветра:* {wind_speed} м/с\n"
            f"☁️ *Описание:* {description.capitalize()}")




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
