from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.inline import filters_keyboard
from keyboards.reply import main_keyboard
from services.google_sheets import GoogleSheets
from states.data_states import DateStates
from sql.repo import Repo

project_router = Router()


@project_router.message(F.text == "Проект")
async def stat_project(message: Message, repo: Repo):
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="stat-project",
                                filters=project_filters,
                                current=0)
    await message.answer(text="Выберите фильтр", reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("stat-project_next"))
async def next(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    project_filters = await repo.get_all_project_filters()
    if current >= len(project_filters) or len(project_filters) <= 8:
        return await call.answer(text="Дальше ничего нету")
    current += 8
    keyboard = filters_keyboard(prefix="stat-project",
                                filters=project_filters,
                                current=current)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("stat-project_back"))
async def back(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    if current == 0:
        return await call.answer(text="Там ничего нету")
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="stat-project",
                                filters=project_filters,
                                current=current-8)
    await call.message.edit_text(text=f"{current-8}--{current}",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("stat-project"))
async def get_date(call: CallbackQuery, state: FSMContext, repo: Repo):
    await call.message.answer(text="Введите дату в формате: день/месяц/год")
    await state.set_state(DateStates.project)
    await state.update_data({"filter": call.data.split("_")[-1]})


@project_router.message(StateFilter(DateStates.project))
async def get_stats(message: Message, state: FSMContext, repo: Repo):
    gs = GoogleSheets()
    filter_id = (await state.get_data())["filter"]
    project_filter = await repo.get_project_filter(filter_id=filter_id)
    stats = await gs.filter(filter=project_filter.filter,
                            date=message.text)
    if not stats:
        return await message.answer(text="Лист с указаной датой не найден")
    text = (f"{project_filter.name}\n"
            f"Спенд: {stats[0]}\n"
            f"Пдп: {stats[1]}\nЦена пдп: {stats[2]}")
    await message.answer(text=text, reply_markup=main_keyboard)
