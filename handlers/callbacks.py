from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from data.loader import dp, bot, node
from keyboards.inlinekeyboards import get_ikb, get_ikb_vm, get_config_ikb_vm, get_storages_for_choice_ikb_vm, get_disks_ikb_vm
from utils.vms import get_vm_info
from handlers.states import ChangeCPUStep, ChangeRAMStep, CreateDiskStep, ResizeDiskStep

@dp.callback_query_handler()
async def choice_mode_city_positions(call: CallbackQuery, state: FSMContext):
    call_dict = dict(call)
    call_back_data = call_dict["data"]

    if "ikb_vm_" in call_back_data:
        vmid = int(call_back_data.split("_")[-1])
        vmname = node.get_vm_name(vmid)
        vm_info = get_vm_info(vmid)
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
        vmid = int(call_back_data.split("_")[-1])
        vm_info = get_vm_info(vmid)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=vm_info,
                               reply_markup=get_config_ikb_vm(vmid),
                               parse_mode='HTML')
        
    elif call_back_data.startswith("change_cpu"):
        vmid = int(call_back_data.split("_")[-1])
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"Введите новое значение CPU для VM {vmid}:")
        await state.update_data(vmid=vmid)
        await ChangeCPUStep.waiting_for_new_cpu.set()

    elif call_back_data.startswith("change_ram"):
        vmid = int(call_back_data.split("_")[-1])
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"Введите новое значение памяти (GB) для VM {vmid}:")
        await state.update_data(vmid=vmid)
        await ChangeRAMStep.waiting_for_new_ram.set()

    elif call_back_data.startswith("resize_disk"):
        vmid = int(call_back_data.split("_")[-1])
        await bot.send_message(chat_id=call.message.chat.id,
                               text="Выберите диск",
                               reply_markup=get_disks_ikb_vm(vmid),
                               parse_mode='HTML')

    elif call_back_data.startswith("choise_disk_resize_"):
        vmid = int(call_back_data.split("_")[-1])
        disk = call_back_data.split("_")[-2]

        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"Введите насколько увеличить диск {disk} в GB для ВМ {vmid}:")

        await state.update_data(vmid=vmid, disk=disk)
        await ResizeDiskStep.waiting_for_increment.set()
        

    elif call_back_data.startswith("add_new_disk_"):
        vmid = int(call_back_data.split("_")[-1])
        await bot.send_message(chat_id=call.message.chat.id,
                               text="Выберете storage:",
                               reply_markup=get_storages_for_choice_ikb_vm(),
                               parse_mode='HTML')
        
        await state.update_data(vmid=vmid)

    elif call_back_data.startswith("choice_storage_"):
        storage = call_back_data.split("_")[-1]
        user_data = await state.get_data()
        print(user_data)
        vmid = user_data['vmid']
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"Введите размер нового диска в GB для ВМ {vmid}:")

        await state.update_data(storage=storage)
        await CreateDiskStep.waiting_for_disk_value.set()
