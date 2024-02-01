from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.inline import filters_keyboard
from keyboards.reply import main_keyboard
from services.google_sheets import GoogleSheets
from states.data_states import DateStates
from sql.repo import Repo

geo_router = Router()


@geo_router.message(F.text == "Гео")
async def stat_geo(message: Message, repo: Repo):
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="stat-geo",
                                filters=geo_filters,
                                current=0)
    await message.answer(text="Выберите фильтр", reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("stat-geo_next"))
async def next(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    geo_filters = await repo.get_all_geo_filters()
    if current >= len(geo_filters) or len(geo_filters) <= 8:
        return await call.answer(text="Дальше ничего нету")
    current += 8
    keyboard = filters_keyboard(prefix="stat-geo",
                                filters=geo_filters,
                                current=current)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("stat-geo_back"))
async def back(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    if current == 0:
        return await call.answer(text="Там ничего нету")
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="stat-geo",
                                filters=geo_filters,
                                current=current-8)
    await call.message.edit_text(text=f"{current-8}--{current}",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("stat-geo"))
async def get_date(call: CallbackQuery, state: FSMContext, repo: Repo):
    await call.message.answer(text="Введите дату в формате: день/месяц/год")
    await state.set_state(DateStates.geo)
    await state.update_data({"filter": call.data.split("_")[-1]})


@geo_router.message(StateFilter(DateStates.geo))
async def get_stats(message: Message, state: FSMContext, repo: Repo):
    gs = GoogleSheets()
    filter_id = (await state.get_data())["filter"]
    geo_filter = await repo.get_geo_filter(filter_id=filter_id)
    stats = await gs.filter(filter=geo_filter.filter,
                            date=message.text)
    if not stats:
        return await message.answer(text="Лист с указаной датой не найден")
    text = (f"{geo_filter.name}\n"
            f"Спенд: {stats[0]}\n"
            f"Пдп: {stats[1]}\nЦена пдп: {stats[2]}")
    await message.answer(text=text, reply_markup=main_keyboard)
