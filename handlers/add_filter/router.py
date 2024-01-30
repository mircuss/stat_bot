from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import generate_filters_keyboard
from .add_project import project_router
from .add_buyer import buyer_router
from .add_geo import geo_router

add_filters_router = Router()

add_filters_router.include_routers(project_router, buyer_router, geo_router)


@add_filters_router.message(F.text == "Добавить фильтр")
async def get_filter_group_to_add(message: Message):
    keyboard = generate_filters_keyboard(prefix="add")
    await message.answer(text="Выберите какой фтльтр хотите добавть",
                         reply_markup=keyboard)
