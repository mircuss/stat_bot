from aiogram import F, Router
from aiogram.types import Message
from keyboards.inline import generate_filters_keyboard
from .delete_geo import geo_router
from .delete_buyer import buyer_router
from .delete_project import project_router

delete_filter_router = Router()

delete_filter_router.include_routers(geo_router, buyer_router, project_router)


@delete_filter_router.message(F.text == "Удалить фильтр")
async def choise_filter_group_to_delete(message: Message):
    keyboard = generate_filters_keyboard(prefix="delete")
    await message.answer(text="Выберите категорию фильтров",
                         reply_markup=keyboard)
