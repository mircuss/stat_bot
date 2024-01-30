from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.filters_states import FilterStates
from keyboards.reply import main_keyboard
from keyboards.inline import back_button
from sql.repo import Repo


project_router = Router()


@project_router.callback_query(F.data == "add_project")
async def get_projectname(call: CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.project)
    await call.message.answer(text="Введите имя Проекта",
                              reply_markup=back_button)
    await call.answer()


@project_router.message(StateFilter(FilterStates.project))
async def add_project(message: Message, repo: Repo, state: FSMContext):
    filter = name = message.text
    if len(name) > 20:
        name = f"{filter[:16]}..."
    await repo.add_project(name=name, filter=filter)
    await message.answer(text="Фильтр проекта добавлено",
                         reply_markup=main_keyboard)
    await state.clear()
