from aiogram import types
from aiogram.dispatcher import FSMContext
from data.loader import dp, bot, node
from keyboards.inlinekeyboards import get_ikb

@dp.message_handler(lambda message: message.text.lower() == 'cancel' or message.text.startswith('/cancel'), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id=message.chat.id,
                            text='Virtual machines:',
                            reply_markup=get_ikb(),
                            parse_mode='HTML')

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=node.status(),
                           reply_markup=kb,
                           parse_mode='HTML')
    await bot.send_message(chat_id=message.chat.id,
                            text='Virtual machines:',
                            reply_markup=get_ikb(),
                            parse_mode='HTML')

@dp.message_handler()
async def messages(message: types.Message):
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
