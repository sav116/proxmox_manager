from aiogram import executor
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from data.loader import dp, bot, node
from keyboards.keyboard import kb
from utils.notify_admins import on_startup_notify
# from keyboards.inlinekeyboards import ikb


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=node.status(),
                           reply_markup=kb,
                           parse_mode='HTML')


# @dp.callback_query_handler()
# async def choice_mode_city_positions(call: CallbackQuery):
#     call_data = dict(call)
#     # print(call_data)
#     product_id = int(call["message"]["caption_entities"][1]["url"].split('/')[-3])
#     report_type = call.data
#     file_path = get_report_path(product_id=product_id, report_type=report_type)
#     # await bot.send_document(chat_id=call.message.chat.id,
#     #                         document=open(file_path, 'rb'))


@dp.message_handler()
async def messages(message: Message):
    
    if message.text == "Виртуальные машины":
        await bot.send_message(chat_id=message.chat.id,
                               text="dev",
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