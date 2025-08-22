# bot.py
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import os

# Токен бота из ENV (обязательно), хардкод убран
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

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

# /refresh — отправить новую кнопку ещё раз
@dp.message(Command("refresh"))
async def refresh(message: types.Message):
    await start(message)

# /url — показать текущий URL
@dp.message(Command("url"))
async def show_url(message: types.Message):
    await message.answer(f"WEBAPP_URL: {WEBAPP_URL}")

# /menu — принудительно обновить кнопку меню
@dp.message(Command("menu"))
async def set_menu(message: types.Message):
    try:
        await bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(text="Открыть приложение", web_app=WebAppInfo(url=WEBAPP_URL))
        )
        await message.answer("Кнопка меню обновлена")
    except Exception as e:
        await message.answer(f"Ошибка обновления меню: {e}")

async def main():
    # Обновляем кнопку меню на новый WebApp URL
    try:
        await bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(text="Открыть приложение", web_app=WebAppInfo(url=WEBAPP_URL))
        )
        logging.info("Chat menu button updated via API")
    except Exception as e:
        logging.error(f"Failed to set chat menu button: {e}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())