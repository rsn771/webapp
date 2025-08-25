import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types.input_file import URLInputFile


BOT_TOKEN = "8340480268:AAEBltqdgQDxwPI_xbRXhOQmvUefBQAambU"


router = Router()


def make_step1_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Далее", callback_data="go_step1")]]
    )


def make_step2_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Далее", callback_data="go_step2")]]
    )


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет Рома, хоть ты и на данный момент не интересуешься криптой, технологиями и тд. я считаю лишним в наше время это точно не будет. Я уверен что когда нибудь ты точно найдешь этому применение ",
        reply_markup=make_step1_keyboard(),
    )


@router.callback_query(F.data == "go_step1")
async def handle_step1(callback: CallbackQuery, bot: Bot) -> None:
    # Удаляем предыдущее сообщение с кнопкой
    try:
        await bot.delete_message(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id
        )
    except Exception:
        # Игнорируем, если уже удалено или нет прав
        pass

    await callback.message.answer(
        "Поскольку в ближайшее время тебе врядли понадобится использовать крипту, я посчитал что биткоин будет лучшим вариантом. Чем дольше лежит- тем больше растет, биткоин рано или поздно всегда поднимается вверх, поэтому этот актив хорошо подойдет под тебя",
        reply_markup=make_step2_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "go_step2")
async def handle_step2(callback: CallbackQuery) -> None:
    await callback.answer()

    # Удаляем предыдущее сообщение с кнопкой перед отправкой фото и кода
    try:
        await callback.message.delete()
    except Exception:
        pass

    photo = URLInputFile("https://picsum.photos/seed/telegram-bot/900/500")
    await callback.message.answer_photo(photo=photo, caption="Вот ваше изображение")

    code_block = """
<pre><code>#!/usr/bin/env bash
echo "This is a code block"
# Скопируй текст нажатием и используй
</code></pre>
""".strip()

    await callback.message.answer(code_block)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

