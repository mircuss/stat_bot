from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.filters_states import FilterStates
from keyboards.reply import main_keyboard
from keyboards.inline import back_button
from sql.repo import Repo


geo_router = Router()


@geo_router.callback_query(F.data == "add_geo")
async def get_geoname(call: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.geo)
    await call.message.edit_text(text="Введите имя Гео",
                                 reply_markup=back_button)
    await call.answer()


@geo_router.message(StateFilter(FilterStates.geo))
async def add_geo(message: Message, repo: Repo, state: FSMContext):
    filter = name = message.text
    if len(name) > 20:
        name = f"{filter[:20]}"
    await repo.add_geo(name=name, filter=filter)
    await message.answer(text="Фильтр гео добавлено",
                         reply_markup=main_keyboard)
    await state.clear()
