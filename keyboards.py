from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainmenunewsupport = KeyboardButton(text='✉ Задать вопрос')
mainmenuabout = KeyboardButton(text='📚 Про нас')

mainmenu = ReplyKeyboardMarkup(
    keyboard=[[mainmenunewsupport, mainmenuabout]],  # Добавляем кнопки в виде списка списков
    resize_keyboard=True
)

