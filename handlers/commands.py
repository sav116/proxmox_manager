from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from data.loader import dp, bot, node
from keyboards.keyboard import kb
from keyboards.inlinekeyboards import get_ikb

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
