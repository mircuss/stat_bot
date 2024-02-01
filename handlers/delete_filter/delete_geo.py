from aiogram import F, Router
from aiogram.types import CallbackQuery
from sql.repo import Repo
from keyboards.inline import filters_keyboard


geo_router = Router()


@geo_router.callback_query(F.data == "delete_geo")
async def choise_geo_filter_to_delete(call: CallbackQuery, repo: Repo):
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="delete-geo",
                                filters=geo_filters,
                                current=0)
    await call.message.edit_text(text="Выберите какой фильтр удалить",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("delete-geo_next"))
async def next(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    geo_filters = await repo.get_all_geo_filters()
    if current >= len(geo_filters) or len(geo_filters) <= 8:
        return await call.answer(text="Дальше ничего нету")
    current += 8
    keyboard = filters_keyboard(prefix="delete-geo",
                                filters=geo_filters,
                                current=current+8)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("delete-geo_back"))
async def back(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    if current == 0:
        return await call.answer(text="Там ничего нету")
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="delete-geo",
                                filters=geo_filters,
                                current=current-8)
    await call.message.edit_text(text=f"{current-8}--{current}",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("delete-geo"))
async def delete_geo(call: CallbackQuery, repo: Repo):
    geo_id = call.data.split("_")[-1]
    await repo.delet_geo_filter(filter_id=geo_id)
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="delete-geo",
                                filters=geo_filters,
                                current=0)
    await call.message.answer(text="Фильтр успешно удалён",
                              reply_markup=keyboard)
    await call.answer()
