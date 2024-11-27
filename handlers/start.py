from aiogram import Router, types
from aiogram.filters import Command


start_router = Router()


@start_router.message(Command("start"))
async def start(message: types.Message):
    name = message.from_user.first_name

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Отправить домашку", callback_data="dz")]
        ]
    )

    await message.answer(
        f"Привет, {name}\n\n" f"Ты попал в бота для отправки домашнего задания",
        reply_markup=kb,
    )
