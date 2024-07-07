from aiogram import executor
from aiogram.types import Message, CallbackQuery


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.loader import dp, bot, node
from keyboards.keyboard import kb
from utils.notify_admins import on_startup
from utils.vms import get_vm_info
from keyboards.inlinekeyboards import get_ikb, get_ikb_vm


class CreateVMStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_id = State()
    waiting_for_cores = State()
    waiting_for_memory = State()

@dp.message_handler(lambda message: message.text.lower() == 'cancel' or message.text.startswith('/cancel'), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id=message.chat.id,
                            text='Virtual machines:',
                            reply_markup=get_ikb(),
                            parse_mode='HTML')
    
# Обработчик команды Create VM
@dp.message_handler(lambda message: message.text == "Create VM")
async def create_vm_start(message: Message):
    await message.answer("Введите название ВМ:")
    await CreateVMStates.waiting_for_name.set()

# Ввод названия ВМ
@dp.message_handler(state=CreateVMStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(vm_name=message.text)
    await message.answer("Введите ID ВМ:")
    await CreateVMStates.waiting_for_id.set()

# Ввод ID ВМ
@dp.message_handler(state=CreateVMStates.waiting_for_id)
async def process_id(message: Message, state: FSMContext):
    await state.update_data(vm_id=message.text)
    await message.answer("Введите количество ядер:")
    await CreateVMStates.waiting_for_cores.set()

# Ввод количества ядер
@dp.message_handler(state=CreateVMStates.waiting_for_cores)
async def process_cores(message: Message, state: FSMContext):
    await state.update_data(vm_cores=message.text)
    await message.answer("Введите количество памяти (GB):")
    await CreateVMStates.waiting_for_memory.set()

# Ввод количества памяти
@dp.message_handler(state=CreateVMStates.waiting_for_memory)
async def process_memory(message: Message, state: FSMContext):
    await state.update_data(vm_memory=message.text)

    user_data = await state.get_data()
    vm_name = user_data['vm_name']
    vm_id = user_data['vm_id']
    vm_cores = user_data['vm_cores']
    vm_memory = int(user_data['vm_memory']) * 1024

    await message.answer("ВМ создаётся ...")
    await state.finish()
    # Вызов функции для создания ВМ
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

@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=node.status(),
                           reply_markup=kb,
                           parse_mode='HTML')
    await bot.send_message(chat_id=message.chat.id,
                            text='Virtual machines:',
                            reply_markup=get_ikb(),
                            parse_mode='HTML')

@dp.callback_query_handler()
async def choice_mode_city_positions(call: CallbackQuery):
    call_dict = dict(call)
    call_back_data = call_dict["data"]

    if "ikb_vm_" in call_back_data:
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        vm_info = get_vm_info(vmid)
        #await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=vm_info,
                               reply_markup=get_ikb_vm(vmid),
                               parse_mode='HTML')

    elif call_back_data.startswith("update_vm_buttons"):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Virtual machines:',
                               reply_markup=get_ikb(),
                               parse_mode='HTML')
        
    elif call_back_data.startswith("reboot"):
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        node.reboot_vm(vmid)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} перезагружается",
                               parse_mode='HTML')

    elif call_back_data.startswith("shutdown"):
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        node.shutdown_vm(vmid)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} выключается",
                               parse_mode='HTML')

    elif call_back_data.startswith("start"):
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        node.start_vm(vmid)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} включается",
                               parse_mode='HTML')

    elif call_back_data.startswith("delete"):
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        node.delete_vm(vmid)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} удаляется ...",
                               parse_mode='HTML')
        await bot.send_message(chat_id=call.message.chat.id,
                                text='Virtual machines:',
                                reply_markup=get_ikb(),
                                parse_mode='HTML')
        
    elif call_back_data.startswith("configure"):
        #await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(call.id, text="Эта опция ещё разработке", show_alert=False)
        
        
@dp.message_handler()
async def messages(message: Message):

    if message.text == "VM's":
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text='Virtual machines:',
                               reply_markup=get_ikb(),
                               parse_mode='HTML')

    elif message.text == "Storage":

        storage_info_list = node.get_storages_info()
        message_storage_info = f"{'='*40}\n".join(storage_info_list)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text=message_storage_info,
                               parse_mode='HTML')
    
    elif message.text == "Power on k8s":
        node.start_k8s()
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="k8s включается...",
                               parse_mode='HTML')
    
    elif message.text == "Reboot node":
        node.reboot()
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="Нода перезагружается...",
                               parse_mode='HTML')
        
    elif message.text == "Shutdown node":
        node.shutdown()
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="Нода выключается...",
                               parse_mode='HTML')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)