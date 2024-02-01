from aiogram.fsm.state import State, StatesGroup


class DateStates(StatesGroup):
    geo = State()
    buyer = State()
    project = State()
