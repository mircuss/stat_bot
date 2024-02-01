from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
        InlineKeyboardButton(text="Назад⬅️", callback_data="back_button")
    ]
])


def filters_keyboard(prefix: str, filters: list, current):
    keyboard = []
    for filter in filters[current:current+8]:
        keyboard.append([
            InlineKeyboardButton(text=filter.name,
                                 callback_data=f"{prefix}_{filter.id}")
        ])
    keyboard.append([InlineKeyboardButton(
                        text="⬅️",
                        callback_data=f"{prefix}_back_{current}"),
                     InlineKeyboardButton(
                        text="➡️",
                        callback_data=f"{prefix}_next_{current}")])
    keyboard.append([InlineKeyboardButton(text="В меню",
                                          callback_data="back_button")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
