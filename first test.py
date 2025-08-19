# bot.py
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import os

API_TOKEN = "8302025614:AAEJPgUpyaldKm25JKvyebDC7ekxFBoIp9A"  # токен бота от @BotFather

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⭐ Купить звёзды",
            web_app=WebAppInfo(url="http://localhost:63342/111/mini%20app%20tg/index.html?_ijt=29jsqbcad8dltfseru2t0atctd&_ij_reload=RELOAD_ON_SAVE")  # тут будет твой мини-сайт
        )]
    ])
    await message.answer("Привет! Это мини-приложение для покупки звёзд:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())