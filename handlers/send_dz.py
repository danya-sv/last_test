from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from bot_config import database


send_dz_router = Router()


class Dz(StatesGroup):
    name = State()
    group_dz = State()
    number_dz = State()
    link = State()


@send_dz_router.callback_query(F.data == "dz")
async def start_dz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Dz.name)
    await callback.message.answer("Для начала введи свое имя")


@send_dz_router.message(Dz.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dz.group_dz)

    group_kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Группа 43-1"),
                types.KeyboardButton(text="Группа 44-1"),
            ],
            [
                types.KeyboardButton(text="Группа 45-1"),
                types.KeyboardButton(text="Группа 46-1"),
            ],
            [
                types.KeyboardButton(text="Группа 47-1"),
                types.KeyboardButton(text="Группа 48-1"),
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer("Теперь введи название своей группы", reply_markup=group_kb)


@send_dz_router.message(Dz.group_dz)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_dz=message.text)
    await state.set_state(Dz.number_dz)
    await message.answer("Теперь введи номер дзшки (от 1 до 8)")


@send_dz_router.message(Dz.number_dz)
async def process_num_dz(message: types.Message, state: FSMContext):
    number_dz = message.text

    if number_dz.isdigit():
        number_dz = int(number_dz)
        
        if number_dz >= 1 and number_dz <= 8:
            await state.update_data(number_dz=number_dz)
            await state.set_state(Dz.link)
            await message.answer("Теперь введи ссылку на свой гит")
        else:
            await message.answer("Номер дзшки должен быть от 1 до 8. Пожалуйста, попробуй снова.")
    else:
        await message.answer("Это не число! Пожалуйста, введи номер домашки от 1 до 8.")


@send_dz_router.message(Dz.link)
async def process_link(message: types.Message, state: FSMContext):
    link = message.text

    if link.startswith("https://github.com"):
        await state.update_data(link=link)
        await message.answer("Дз успешно отправлено")
        data = await state.get_data()
        
        database.execute(
            query=""" 
            INSERT INTO homework (name, group_dz, number_dz, link)
            VALUES (?, ?, ?, ?)
            """,
            params=(data["name"], data["group_dz"], data["number_dz"], data["link"]),
        )

        await state.clear()
    else:
        await message.answer("Ссылка должна начинаться с 'https://github.com'. Пожалуйста, попробуй снова.")

