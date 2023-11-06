from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем кнопки
button1 = KeyboardButton("VM's")
button2 = KeyboardButton("Power on k8s")
button3 = KeyboardButton("Reboot node")
button4 = KeyboardButton("Shutdown node")
button5 = KeyboardButton("Create VM")

# Создаем клавиатуру и добавляем кнопки
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(button1, button2, button5)
kb.add(button3, button4)