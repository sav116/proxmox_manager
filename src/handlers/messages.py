from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from data.loader import dp, bot, node
from keyboards.inlinekeyboards import get_ikb
from utils.vms import get_vm_info
from states.change_cpu import ChangeCPUStep
from states.change_ram import ChangeRAMStep
from states.create_vm import CreateVMStates

@dp.message_handler(state=ChangeRAMStep.waiting_for_new_ram, content_types=ContentTypes.TEXT)
async def process_new_ram_value(message: Message, state: FSMContext):
    new_ram_value = message.text
    if not new_ram_value.isdigit():
        await message.reply("Введите количество памяти (GB):")
        return

    new_ram_value_mb = int(new_ram_value) * 1024
    user_data = await state.get_data()
    vmid = user_data['vmid']
    
    node.update_vm_config(vmid, memory=new_ram_value_mb)
    
    await message.reply(f"Значение памяти для VM {vmid} обновлено до {new_ram_value}Gb.")

    await state.finish()

@dp.message_handler(state=ChangeCPUStep.waiting_for_new_cpu, content_types=ContentTypes.TEXT)
async def process_new_cpu_value(message: Message, state: FSMContext):
    new_cpu_value = message.text
    if not new_cpu_value.isdigit():
        await message.reply("Введите количество ядер CPU:")
        return

    new_cpu_value = int(new_cpu_value)
    user_data = await state.get_data()
    vmid = user_data['vmid']
    
    node.update_vm_config(vmid, cores=new_cpu_value)
    
    await message.reply(f"Количество ядер CPU для VM {vmid} обновлено до {new_cpu_value}.")

    # Завершаем состояние
    await state.finish()

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

@dp.message_handler(lambda message: message.text == "Create VM")
async def create_vm_start(message: Message):
    await message.answer("Введите название ВМ:")
    await CreateVMStates.waiting_for_name.set()

@dp.message_handler(state=CreateVMStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(vm_name=message.text)
    await message.answer("Введите ID ВМ:")
    await CreateVMStates.waiting_for_id.set()

@dp.message_handler(state=CreateVMStates.waiting_for_id)
async def process_id(message: Message, state: FSMContext):
    await state.update_data(vm_id=message.text)
    await message.answer("Введите количество ядер:")
    await CreateVMStates.waiting_for_cores.set()

@dp.message_handler(state=CreateVMStates.waiting_for_cores)
async def process_cores(message: Message, state: FSMContext):
    await state.update_data(vm_cores=message.text)
    await message.answer("Введите количество памяти (GB):")
    await CreateVMStates.waiting_for_memory.set()

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
