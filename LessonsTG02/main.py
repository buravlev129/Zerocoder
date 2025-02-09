import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from gtts import gTTS
from googletrans import Translator

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


if not os.path.exists('img'):
    os.makedirs('img')
if not os.path.exists('tmp'):
    os.makedirs('tmp')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Я тестовый бот с разными функциями")


@dp.message(Command("help"))
async def help(message: Message):
    bf = """
    Команды:
    /start    - Запустить бота
    /help     - Получить справку по командам
    Дополнительные функции:
     - Сохранение файлов
     - Голосовое сообщение (озвучивает переданный текст)
        *voice:* [какой-то текст]
     - Перевод текста на английский:
        *translate:* [какой-то текст]
    """
    await message.answer(bf, parse_mode=ParseMode.MARKDOWN)


@dp.message(F.photo)
async def save_photo(message: Message):
    photo = message.photo[-1]  # Выбираем фото наибольшего размера
    file_id = photo.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    file = await bot.download_file(file_path)

    file_name = f"img/{file_id}.jpg"
    with open(file_name, 'wb') as f:
        f.write(file.getvalue())

    await message.reply("Фото сохранено!")


@dp.message(F.text.startswith("photo:"))
async def get_photo(message: Message):
    file_name = message.text[6:].strip()
    if file_name:
        file_path = f"img/{file_name}.jpg"
        if os.path.exists(file_path):
            photo = FSInputFile(file_path)
            await message.reply_photo(photo)
        else:
            await message.reply(f"Файл с таким именем не найден. {file_name}")
    else:
        await message.reply("Неверно указано имя файла")


@dp.message(F.text.startswith("voice:"))
async def voice_text(message: Message):
    text = message.text[6:].strip()
    if text:
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_voice")
        file_name = f"tmp/voice-4152525.ogg"
        tts = gTTS(text=text, lang='ru')
        tts.save(file_name)
        audio = FSInputFile(file_name)
        await bot.send_voice(chat_id=message.chat.id, voice=audio)
        os.remove(file_name)        
    else:
        await message.reply("Введите текст для озвучивания в формате:\n voice: [какой-то текст]")


@dp.message(F.text.startswith("translate:"))
async def translate_message(message: Message):
    text = message.text[10:].strip()
    if text:
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        translated = translator.translate(message.text, dest='en')
        await message.reply(translated.text)
    else:
        await message.reply("Введите текст для перевода в формате:\n translate: [какой-то текст]")



@dp.message()
async def any_message(message: Message):
    await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
