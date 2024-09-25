import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv

from common.bot_cmds_list import private_commands
from handler import user_handler, user_group_handler

ALLOWED_UPDATES = ['message, edited_message']
load_dotenv()

logging.basicConfig(level=logging.INFO)



async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user_handler.router, user_group_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())


""" Задаем команды через бот фазера
start - Запустить бота
menu - Посмотреть меню
about - О бренде
about_bot - О боте
help - Чат с тех. поддержкой
"""