from aiogram import F, Router
from aiogram.types import CallbackQuery
from sql.repo import Repo
from keyboards.inline import filters_keyboard


project_router = Router()


@project_router.callback_query(F.data == "delete_project")
async def choise_project_filter_to_delete(call: CallbackQuery, repo: Repo):
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters)
    await call.message.edit_text(text="Выберите какой фильтр удалить",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("delete-project"))
async def delete_project(call: CallbackQuery, repo: Repo):
    project_id = call.data.split("_")[-1]
    await repo.delet_project_filter(filter_id=project_id)
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters)
    await call.message.answer(text="Фильтр успешно удалён",
                              reply_markup=keyboard)
    await call.answer()
