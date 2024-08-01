import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import start_head

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# Запуск бота
async def main():
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher()
    dp.include_router(start_head.router)
    try:
        # Удаление вебхуков и очистка накопленных обновлений
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при удалении вебхуков: {e}")

    try:
        # Запуск бота с поллингом
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске поллинга: {e}")


if __name__ == "__main__":
    asyncio.run(main())