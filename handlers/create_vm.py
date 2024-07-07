from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.loader import dp, node, bot
from keyboards.inlinekeyboards import get_ikb

class CreateVMStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_id = State()
    waiting_for_cores = State()
    waiting_for_memory = State()

@dp.message_handler(lambda message: message.text == "Create VM")
async def create_vm_start(message: types.Message):
    await message.answer("Введите название ВМ:")
    await CreateVMStates.waiting_for_name.set()

@dp.message_handler(state=CreateVMStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(vm_name=message.text)
    await message.answer("Введите ID ВМ:")
    await CreateVMStates.waiting_for_id.set()

@dp.message_handler(state=CreateVMStates.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    await state.update_data(vm_id=message.text)
    await message.answer("Введите количество ядер:")
    await CreateVMStates.waiting_for_cores.set()

@dp.message_handler(state=CreateVMStates.waiting_for_cores)
async def process_cores(message: types.Message, state: FSMContext):
    await state.update_data(vm_cores=message.text)
    await message.answer("Введите количество памяти (GB):")
    await CreateVMStates.waiting_for_memory.set()

@dp.message_handler(state=CreateVMStates.waiting_for_memory)
async def process_memory(message: types.Message, state: FSMContext):
    await state.update_data(vm_memory=message.text)
    user_data = await state.get_data()
    vm_name = user_data['vm_name']
    vm_id = user_data['vm_id']
    vm_cores = user_data['vm_cores']
    vm_memory = int(user_data['vm_memory']) * 1024
    await message.answer("ВМ создаётся ...")
    await state.finish()
    node.create_vm_from_template(
        vmname=vm_name,
        template_name='alma-template-32g',
        vmid=vm_id,
        cores=vm_cores,
        memory=vm_memory,
        )
    await message.answer(f"ВМ {vm_name} с id {vm_id} создана")
    await bot.send_message(chat_id=message.chat.id,
                            text='Virtual machines:',
                            reply_markup=get_ikb(),
                            parse_mode='HTML')
