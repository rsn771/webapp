# bot.py
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import os

API_TOKEN = "8302025614:AAEJPgUpyaldKm25JKvyebDC7ekxFBoIp9A"  # токен бота от @BotFather

# URL мини-приложения из ENV, с безопасным дефолтом
WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "https://webapp-git-cursor-bc-7d4a93bc-8-a545c2-playm4798-7284s-projects.vercel.app/"
)

logging.basicConfig(level=logging.INFO)
logging.info(f"Using WEBAPP_URL={WEBAPP_URL}")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    logging.info(f"Sending keyboard with WEBAPP_URL={WEBAPP_URL}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⭐ Купить звёзды",
            web_app=WebAppInfo(url=WEBAPP_URL)  # прод-домен мини-приложения
        )]
    ])
    await message.answer("Привет! Это мини-приложение для покупки звёзд:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())