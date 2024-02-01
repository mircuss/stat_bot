from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.filters_states import FilterStates
from keyboards.reply import main_keyboard
from keyboards.inline import back_button
from sql.repo import Repo

buyer_router = Router()


@buyer_router.callback_query(F.data == "add_buyer")
async def get_buyername(call: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.buyer)
    await call.message.answer(text="Введите имя Баера",
                              reply_markup=back_button)
    await call.answer()


@buyer_router.message(StateFilter(FilterStates.buyer))
async def add_buyer(message: Message, repo: Repo, state: FSMContext):
    filter = name = message.text
    if len(name) > 20:
        name = f"{filter[:20]}"
    await repo.add_buyer(name=name, filter=filter)
    await message.answer(text="Фильтр баера добавлено",
                         reply_markup=main_keyboard)
    await state.clear()
