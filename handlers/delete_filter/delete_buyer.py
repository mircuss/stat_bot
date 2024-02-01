from aiogram import F, Router
from aiogram.types import CallbackQuery
from sql.repo import Repo
from keyboards.inline import filters_keyboard

buyer_router = Router()


@buyer_router.callback_query(F.data == "delete_buyer")
async def choise_buyer_filter_to_delete(call: CallbackQuery, repo: Repo):
    buyer_filters = await repo.get_all_buyer_filters()
    keyboard = filters_keyboard(prefix="delete-buyer",
                                filters=buyer_filters,
                                current=0)
    await call.message.edit_text(text="Выберите какой фильтр удалить",
                                 reply_markup=keyboard)


@buyer_router.callback_query(F.data.startswith("delete-buyer"))
async def delete_buyer(call: CallbackQuery, repo: Repo):
    buyer_id = call.data.split("_")[-1]
    await repo.delet_buyer_filter(filter_id=buyer_id)
    buyer_filters = await repo.get_all_buyer_filters()
    keyboard = filters_keyboard(prefix="delete-buyer",
                                filters=buyer_filters,
                                current=0)
    await call.message.answer(text="Фильтр успешно удалён",
                              reply_markup=keyboard)
    await call.answer()
