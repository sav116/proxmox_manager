from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем кнопки
button1 = KeyboardButton("VM's")
button2 = KeyboardButton("Power on k8s")
button3 = KeyboardButton("Reboot node")
button4 = KeyboardButton("Shutdown node")
button5 = KeyboardButton("Create VM")
button6 = KeyboardButton("Cancel")

# Создаем клавиатуру и добавляем кнопки
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(button1, button5, button6)
kb.add(button2, button3, button4)