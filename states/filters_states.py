from aiogram.fsm.state import State, StatesGroup


class FilterStates(StatesGroup):
    geo = State()
    buyer = State()
    project = State()
