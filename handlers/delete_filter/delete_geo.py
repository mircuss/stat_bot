from aiogram import F, Router
from aiogram.types import CallbackQuery
from sql.repo import Repo
from keyboards.inline import filters_keyboard


geo_router = Router()


@geo_router.callback_query(F.data == "delete_geo")
async def choise_geo_filter_to_delete(call: CallbackQuery, repo: Repo):
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="delete-geo", filters=geo_filters)
    await call.message.edit_text(text="Выберите какой фильтр удалить",
                                 reply_markup=keyboard)


@geo_router.callback_query(F.data.startswith("delete-geo"))
async def delete_geo(call: CallbackQuery, repo: Repo):
    geo_id = call.data.split("_")[-1]
    await repo.delet_geo_filter(filter_id=geo_id)
    geo_filters = await repo.get_all_geo_filters()
    keyboard = filters_keyboard(prefix="delete-geo",
                                filters=geo_filters)
    await call.message.answer(text="Фильтр успешно удалён",
                              reply_markup=keyboard)
    await call.answer()
