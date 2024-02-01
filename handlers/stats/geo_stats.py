from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboards.inline import filters_keyboard
from services.google_sheets import GoogleSheets
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
async def get_stats(call: CallbackQuery, repo: Repo):
    gs = GoogleSheets()
    filter_id = int(call.data.split("_")[-1])
    geo_filter = await repo.get_geo_filter(filter_id=filter_id)
    stats = await gs.filter_geo(filter=geo_filter.filter,
                                date=None)
    text = (f"{geo_filter.name}\n"
            f"Спенд: {stats[0]}\n"
            f"Пдп: {stats[1]}\nЦена пдп: {round(stats[2], 3)}")
    await call.message.edit_text(text=text)
