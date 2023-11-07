from aiogram import executor
from aiogram.types import Message, CallbackQuery

from data.loader import dp, bot, node
from keyboards.keyboard import kb
from utils.notify_admins import on_startup_notify, on_startup
from utils.vms import get_vm_info
from keyboards.inlinekeyboards import get_ikb, get_ikb_vm


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=node.status(),
                           reply_markup=kb,
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

    elif message.text == "Create VM":
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text="Опция ещё в разработке",
                               parse_mode='HTML')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)