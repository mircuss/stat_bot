from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.reply import (main_keyboard,
                             edit_filters_keyboard,
                             stats_group_keyboard)
from sql.repo import Repo

basic_router = Router()


@basic_router.message(F.text == "/start")
async def start(message: Message, repo: Repo, state: FSMContext):
    await message.answer(text="Добро пожаловать!",
                         reply_markup=main_keyboard)
    await state.clear()


@basic_router.message(F.text == "Редактировать фильтры")
async def edit_filters(message: Message):
    await message.answer(text="Выберите что вы хотите сделать",
                         reply_markup=edit_filters_keyboard)


@basic_router.message(F.text == "Смотреть статистику")
async def choise_stats_group(message: Message):
    await message.answer(text="Выберите категорию статистики",
                         reply_markup=stats_group_keyboard)


@basic_router.callback_query(F.data == "back_button")
async def bac_button(call: CallbackQuery):
    await call.answer()
    await call.message.answer(text="Вы в меню", reply_markup=main_keyboard)
