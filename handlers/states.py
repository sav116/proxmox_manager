from aiogram.dispatcher.filters.state import State, StatesGroup

class ChangeCPUStep(StatesGroup):
    waiting_for_new_cpu = State()

class ChangeRAMStep(StatesGroup):
    waiting_for_new_ram = State()

class CreateDiskStep(StatesGroup):
    waiting_for_disk_value  = State()

class ResizeDiskStep(StatesGroup):
    waiting_for_increment = State()

class CreateVMStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_id = State()
    waiting_for_cores = State()
    waiting_for_memory = State()