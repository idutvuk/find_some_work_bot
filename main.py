import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TELEGRAM_BOT_TOKEN
from telegram_handlers import router
from telethon_polling import poll_channels


logging.basicConfig(
    format="%(asctime)s|%(name)s|%(levelname)s | %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(poll_channels(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
