from aiogram import Bot, Dispatcher

from config.config import Config, get_env_values
from services.update_products import reupdate_db
from handlers.user_handler import user_router
import logging
import asyncio

logger = logging.getLogger(__name__)

async def main() -> None:
    # раскоменнтировать, чтобы обновить базу данных
    # reupdate_db()

    env_values: Config = get_env_values('.env')
    
    logging.basicConfig(
         level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot...')

    bot = Bot(token=env_values.TgBot.token)
    dp = Dispatcher()

    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())