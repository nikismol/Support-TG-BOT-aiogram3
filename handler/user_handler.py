import os
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from dotenv import load_dotenv

load_dotenv()
router = Router()
CHAT_ID = os.getenv('CHAT_ID')

def get_user_data(message: Message) -> str:
    return (f'{message.from_user.id}\n'  # Сохраняем ID пользователя
            f'{message.from_user.first_name or "Имя отсутствует."}\n'
            f'{message.from_user.last_name or "Фамилия отсутствует."}\n\n')


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f'Добрый день, {message.from_user.first_name if message.from_user.first_name is not None else message.from_user.username}.\nБот запущен.\n')


@router.message()
async def echo_handler(message: Message) -> None:
    await message.answer(message.text)



# @router.message(F.text)
# async def send_to_admin(message: Message, state: FSMContext):
#     user_data = get_user_data(message)
#     text_message = message.text if message.text is not None else "Сообщение без текста."
#     message_for_admin = user_data + text_message
#
#     await message.bot.send_message(
#         chat_id=CHAT_ID,
#         text=message_for_admin,  # Отправляем администратору сообщение с ID пользователя
#     )
