from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboards.inline import filters_keyboard
from services.google_sheets import GoogleSheets
from sql.repo import Repo

buyer_router = Router()


@buyer_router.message(F.text == "Баер")
async def stat_buyer(message: Message, repo: Repo):
    buyer_filters = await repo.get_all_buyer_filters()
    keyboard = filters_keyboard(prefix="stat-buyer",
                                filters=buyer_filters,
                                current=0)
    await message.answer(text="Выберите фильтр", reply_markup=keyboard)


@buyer_router.callback_query(F.data.startswith("stat-buyer_next"))
async def next(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    buyer_filters = await repo.get_all_buyer_filters()
    if current >= len(buyer_filters) or len(buyer_filters) <= 8:
        return await call.answer(text="Дальше ничего нету")
    current += 8
    keyboard = filters_keyboard(prefix="stat-buyer",
                                filters=buyer_filters,
                                current=current)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@buyer_router.callback_query(F.data.startswith("stat-buyer_back"))
async def back(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    if current == 0:
        return await call.answer(text="Там ничего нету")
    buyer_filters = await repo.get_all_buyer_filters()
    keyboard = filters_keyboard(prefix="stat-buyer",
                                filters=buyer_filters,
                                current=current-8)
    await call.message.edit_text(text=f"{current-8}--{current}",
                                 reply_markup=keyboard)


@buyer_router.callback_query(F.data.startswith("stat-buyer"))
async def get_stats(call: CallbackQuery, repo: Repo):
    gs = GoogleSheets()
    filter_id = int(call.data.split("_")[-1])
    buyer_filter = await repo.get_buyer_filter(filter_id=filter_id)
    stats = await gs.filter_buyer(filter=buyer_filter.filter,
                                  date=None)
    text = (f"{buyer_filter.name}\n"
            f"Спенд: {stats[0]}\n"
            f"Пдп: {stats[1]}\nЦена пдп: {round(stats[2], 3)}")
    await call.message.edit_text(text=text)
