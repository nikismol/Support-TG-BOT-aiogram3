from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from filters.admin_or_user import AdminFilter,UserFilter, admins
import logging

router = Router()

user_messages = {}

logging.basicConfig(level=logging.DEBUG)

@router.message(Command('start'), AdminFilter())
async def admin_start(message: Message):
    await message.reply("Привет, админ! Что вы хотите узнать или сделать?")

@router.message(Command('start'), UserFilter())
async def user_start(message: Message):
    await message.reply("Добрый день")


@router.message(UserFilter())
async def handle_user_message(message: Message):
    user_messages[message.message_id] = message.from_user.id

    logging.info(f"Текущее состояние user_messages: {user_messages}")

    for admin_id in admins:
        try:
            sent_message = await message.bot.send_message(
                chat_id=admin_id,
                text=(f"Сообщение от пользователя {message.from_user.full_name}: {message.text}\n"
                      f"ID сообщения: {message.message_id}\n"
                      f"Ответьте на это сообщение для ответа пользователю.")
            )
            logging.info(f"Сообщение от пользователя отправлено админу {admin_id}. Сообщение ID: {sent_message.message_id}")
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")

    await message.answer("Ваше сообщение отправлено администраторам.")

@router.message(AdminFilter())
async def handle_admin_message(message: Message):

    if message.reply_to_message:
        original_message_id_line = next(
            (line for line in message.reply_to_message.text.split('\n') if line.startswith("ID сообщения: ")),
            None
        )
        if original_message_id_line:
            original_message_id = int(original_message_id_line.split(": ")[1])

            user_id = user_messages.get(original_message_id)

            if user_id:
                logging.info(f"Найден пользователь с ID {user_id} для сообщения ID {original_message_id}")

                try:
                    await message.bot.send_message(chat_id=user_id, text=f"Ответ от администратора: {message.text}")
                    await message.reply("Ваш ответ отправлен пользователю.")
                    logging.info(f"Ответ успешно отправлен пользователю {user_id} на сообщение ID {original_message_id}")
                except Exception as e:
                    logging.error(f"Не удалось отправить ответ пользователю {user_id}: {e}")
            else:
                await message.reply(f"Не удалось найти исходное сообщение. ID сообщения: {original_message_id}")
                logging.warning(f"Не удалось найти пользователя для сообщения ID {original_message_id}")
        else:
            await message.reply("Не удалось извлечь ID оригинального сообщения.")
            logging.warning("Не удалось извлечь ID оригинального сообщения.")
    else:
        await message.reply("Пожалуйста, ответьте на сообщение пользователя.")
        logging.info("Администратор не ответил на сообщение пользователя, отправлено напоминание.")

