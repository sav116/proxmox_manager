from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("Виртуальные машины"))
kb.add(KeyboardButton("Перезагрузить ноду"))
kb.add(KeyboardButton("Выключить ноду"))