from aiogram.dispatcher.filters.state import State, StatesGroup

class CreateVMStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_id = State()
    waiting_for_cores = State()
    waiting_for_memory = State()
