from aiogram import F, Router
from aiogram.types import CallbackQuery
from sql.repo import Repo
from keyboards.inline import filters_keyboard


project_router = Router()


@project_router.callback_query(F.data == "delete_project")
async def choise_project_filter_to_delete(call: CallbackQuery, repo: Repo):
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters,
                                current=0)
    await call.message.edit_text(text="Выберите какой фильтр удалить",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("delete-project_next"))
async def next(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    project_filters = await repo.get_all_project_filters()
    if current >= len(project_filters) or len(project_filters) <= 8:
        return await call.answer(text="Дальше ничего нету")
    current += 8
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters,
                                current=current+8)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("delete-project_back"))
async def back(call: CallbackQuery, repo: Repo):
    current = int(call.data.split("_")[-1])
    if current == 0:
        return await call.answer(text="Там ничего нету")
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters,
                                current=current-8)
    await call.message.edit_text(text=f"{current}--{current+8}",
                                 reply_markup=keyboard)


@project_router.callback_query(F.data.startswith("delete-project"))
async def delete_project(call: CallbackQuery, repo: Repo):
    project_id = call.data.split("_")[-1]
    await repo.delet_project_filter(filter_id=project_id)
    project_filters = await repo.get_all_project_filters()
    keyboard = filters_keyboard(prefix="delete-project",
                                filters=project_filters,
                                current=0)
    await call.message.answer(text="Фильтр успешно удалён",
                              reply_markup=keyboard)
    await call.answer()
