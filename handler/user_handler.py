import os
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()
router = Router()
CHAT_ID = os.getenv('CHAT_ID')

def get_user_data(message: Message) -> str:
    return (f'{message.from_user.id}\n'  # Сохраняем ID пользователя
            f'{message.from_user.first_name or "Имя отсутствует."}\n'
            f'{message.from_user.last_name or "Фамилия отсутствует."}\n\n')


@router.message(F.photo)
async def forward_photo_to_admin(message: Message, state: FSMContext):
    user_data = get_user_data(message)
    caption = message.caption if message.caption else None
    text = user_data + f'Подпись: {caption}'

    await message.bot.send_photo(
        chat_id=CHAT_ID,
        photo=message.photo[-1].file_id,
        caption=text  # Добавляем ID пользователя в подпись
    )

@router.message(F.text)
async def send_to_admin(message: Message, state: FSMContext):
    user_data = get_user_data(message)
    text_message = message.text if message.text is not None else "Сообщение без текста."
    message_for_admin = user_data + text_message

    await message.bot.send_message(
        chat_id=CHAT_ID,
        text=message_for_admin,  # Отправляем администратору сообщение с ID пользователя
    )
