from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeCPUStep(StatesGroup):
    waiting_for_new_cpu = State()
