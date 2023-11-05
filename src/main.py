from aiogram import executor
from aiogram.types import Message, CallbackQuery

from data.loader import dp, bot, node
from keyboards.keyboard import kb
from utils.notify_admins import on_startup_notify
from keyboards.inlinekeyboards import get_ikb, get_ikb_vm



async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


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
    vmid = int(call_back_data.split("_")[-1])
    vmname = node.get_vm_name(vmid)
    
    if "ikb_vm_" in call_back_data:
        await bot.send_message(chat_id=call.message.chat.id,
                               text=vmname,
                               reply_markup=get_ikb_vm(vmid),
                               parse_mode='HTML')
        
    elif call_back_data.startswith("reboot"):
        node.reboot_vm(vmid)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} перезагружается",
                               parse_mode='HTML')

    elif call_back_data.startswith("shutdown"):
        node.shutdown_vm(vmid)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} выключается",
                               parse_mode='HTML')

    elif call_back_data.startswith("start"):
        node.start_vm(vmid)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f"{vmname} включается",
                               parse_mode='HTML')

@dp.message_handler()
async def messages(message: Message):
    
    if message.text == "Виртуальные машины":
        await bot.send_message(chat_id=message.chat.id,
                               text='Virtual machines:',
                               reply_markup=get_ikb(),
                               parse_mode='HTML')
    
    elif message.text == "Включить k8s":
        node.start_k8s()
        await bot.send_message(chat_id=message.chat.id,
                               text="k8s включается...",
                               parse_mode='HTML')
    
    elif message.text == "Перезагрузить ноду":
        node.reboot()
        await bot.send_message(chat_id=message.chat.id,
                               text="Нода перезагружается...",
                               parse_mode='HTML')
        
    elif message.text == "Выключить ноду":
        node.shutdown()
        await bot.send_message(chat_id=message.chat.id,
                               text="Нода выключается...",
                               parse_mode='HTML')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)