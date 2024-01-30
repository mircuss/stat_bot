from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_filters_keyboard(prefix: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Гео",
                                 callback_data=f"{prefix}_geo")
        ],
        [
            InlineKeyboardButton(text="Проект",
                                 callback_data=f"{prefix}_project")
        ],
        [
            InlineKeyboardButton(text="Баер",
                                 callback_data=f"{prefix}_buyer")
        ]
    ])
    return keyboard


back_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад⬅️", callback_data="back")
    ]
])


def filters_keyboard(prefix: str, filters: list):
    keyboard = InlineKeyboardBuilder()
    for filter in filters:
        keyboard.add(
            InlineKeyboardButton(text=filter.name,
                                 callback_data=f"{prefix}_{filter.id}")
        )
    return keyboard.as_markup()
