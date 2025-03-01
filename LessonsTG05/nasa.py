import asyncio
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from googletrans import Translator

from config import TOKEN, NASA_API_KEY
from keyboards import kbd_reply_markup
from datetime import datetime, timedelta
import random



bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()



@dp.message(CommandStart())
async def start(message: Message):
    bf = """
    Привет! Я бот NASA. Вот что я могу:
    /apod - Astronomy Picture of the Day
    /mars - Фотографии с Марса
    /earth - Спутниковый снимок Земли
    """
    await message.answer(bf, reply_markup=kbd_reply_markup)


@dp.message(F.text == "apod")
async def get_apod(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=365)
    random_dt = start_dt + (end_dt - start_dt) * random.random()
    s_dt = random_dt.strftime("%Y-%m-%d")
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={s_dt}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        title = data.get('title', 'No title')
        explanation = data.get('explanation', 'No explanation')
        media_url = data.get('url', '')
        media_type = data.get('media_type', '')

        if media_type == 'image':
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=media_url,
                caption=f"<b>{title}</b>",
                parse_mode=ParseMode.HTML
            )

            translated = translator.translate(explanation, dest='ru')
            await message.answer(translated.text)
        else:
            await message.reply("Не удалось получить картинку")
    else:
        await message.reply("Ошибка при запросе APOD.")


@dp.message(F.text == "mars")
async def get_mars_photos(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={NASA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            photo = photos[0]
            img_url = photo['img_src']
            earth_date = photo['earth_date']
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=img_url,
                caption=f"Фото с Марса (дата: {earth_date})"
            )
        else:
            await message.reply("Фотографии с Марса не найдены.")
    else:
        await message.reply("Ошибка при запросе фотографий с Марса.")


def get_random_eurasia_coordinates():
    min_lat = 10  # Минимальная широта
    max_lat = 80  # Максимальная широта
    min_lon = 10  # Минимальная долгота
    max_lon = 180 # Максимальная долгота

    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)
    return lat, lon


@dp.message(F.text == "earth")
async def get_earth_imagery(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    lat, lon = get_random_eurasia_coordinates()
    url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&date=2023-01-01&api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=url,
            caption=f"Спутниковый снимок Евразии\nКоординаты: {lat:.4f}, {lon:.4f}"
        )
    else:
        await message.reply("Ошибка при запросе спутникового снимка.")




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
