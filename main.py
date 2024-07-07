from aiogram import executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from data.loader import dp, bot, node
from keyboards.keyboard import kb
from utils.notify_admins import on_startup
from keyboards.inlinekeyboards import get_ikb
from handlers import create_vm, change_cpu, change_ram, common

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
