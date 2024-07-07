from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeRAMStep(StatesGroup):
    waiting_for_new_ram = State()
