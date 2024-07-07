from aiogram import executor
from data.loader import dp
from utils.notify_admins import on_startup

# Регистрация обработчиков
from handlers import commands, messages, callbacks

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
