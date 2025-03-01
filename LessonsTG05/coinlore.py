import asyncio
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from itertools import islice
from collections import namedtuple
from tabulate import tabulate

from config import TOKEN
from keyboards import kbd_reply_markup


Crypto = namedtuple("Crypto", ["id", "name", "symbol"])
list_crypto: list[Crypto] = []


BASE_URL = "https://api.coinlore.com/api"

bot = Bot(token=TOKEN)
dp = Dispatcher()



def get_top_cryptocurrencies(start=0, limit=50):
    """
    Получает информацию о топ-N криптовалютах по рыночной капитализации.
    
    :param limit: Количество криптовалют для получения (по умолчанию 10).
    :return: Список словарей с данными о криптовалютах.
    """
    endpoint = f"{BASE_URL}/tickers/"
    params = {
        'start': str(start),  # Начало списка
        'limit': str(limit)   # Количество элементов
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', [])
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return []


def get_crypto_details(crypto_id):
    """
    Получает подробную информацию о криптовалюте по её ID.
    
    :param crypto_id: ID криптовалюты.
    :return: Словарь с данными о криптовалюте.
    """
    endpoint = f"{BASE_URL}/ticker/"
    params = {'id': crypto_id}
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data[0]
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return {}
    

def reload_list_crypto():
    list_crypto.clear()
    lst = get_top_cryptocurrencies(0, 100)
    for crypto in lst:
        list_crypto.append(Crypto(crypto.get('id', 'N/A'), crypto.get('name', 'N/A'), crypto.get('symbol', 'N/A')))



@dp.message(CommandStart())
async def start(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    reload_list_crypto()

    bf = """
    Привет! Я бот CoinLore для получения информации по криптовалютам
    """
    await message.answer(bf, reply_markup=kbd_reply_markup)


@dp.message(Command("list"))
async def process_list_crypto(message: Message):

    if not list_crypto:
        reload_list_crypto()

    if list_crypto:
        bf = []
        for crypto in islice(list_crypto, 50):
            bf.append(crypto)

        table = tabulate(bf, headers=["Id", "Name", "Symbol"], tablefmt="pretty")
        await message.answer(text=f"<pre>{table}</pre>", parse_mode=ParseMode.HTML)
    else:
        await message.answer("Не удалось получить список криптовалют")


def format_crypto_details(crypto_data):

    if not crypto_data:
        return ""
    
    name = crypto_data.get('name', 'N/A')
    symbol = crypto_data.get('symbol', 'N/A')
    price_usd = crypto_data.get('price_usd', 'N/A')
    market_cap = crypto_data.get('market_cap_usd', 'N/A')
    volume_24h = crypto_data.get('volume24', 'N/A')
    percent_change_24h = crypto_data.get('percent_change_24h', 'N/A')
    
    bf = f"""
    <b>Информация о криптовалюте {name} ({symbol}):</b>
          Цена: ${price_usd}
          Рыночная капитализация: ${market_cap}
          Объем торгов за 24 часа: ${volume_24h}
          Изменение цены за 24 часа: {percent_change_24h}%
    """
    return bf


@dp.message()
async def display_crypto_details(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    symbol = message.text.strip()
    crypto = next(filter(lambda x: x.symbol == symbol, list_crypto), None)
    if crypto:
        details = get_crypto_details(crypto.id)

        bf = format_crypto_details(details)
        await message.answer(text=bf, parse_mode=ParseMode.HTML)
    else:
        await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
