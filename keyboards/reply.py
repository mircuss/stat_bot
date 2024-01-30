from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Редактировать фильтры")
    ],
    [
        KeyboardButton(text="Смотреть статистику")
    ]
], resize_keyboard=True)

edit_filters_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить фильтр")
    ],
    [
        KeyboardButton(text="Удалить фильтр")
    ]
], resize_keyboard=True)

stats_group_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Гео")
    ],
    [
        KeyboardButton(text="Проект")
    ],
    [
        KeyboardButton(text="Баер")
    ]
], resize_keyboard=True)
