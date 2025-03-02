import asyncio
import logging
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELETHON_POLLING_INTERVAL
from variables import BotConfig
from openai_filter import filter_match

logger = logging.getLogger(__name__)
config = BotConfig()

telethon_client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def poll_channels(bot):
    """
    Опрос каналов и групп через Telethon.
    Для каждого нового сообщения проверяется фильтр OpenAI и, если сообщение проходит фильтрацию,
    оно пересылается подписчикам через aiogram Bot.
    """
    await telethon_client.start()
    while True:
        config.load_variables()
        for channel in config.channels.keys():
            try:
                messages = await telethon_client.get_messages(channel, limit=1)
                if not messages:
                    continue
                message = messages[0]
                last_id = config.channels.get(channel, 0)
                if message.id <= last_id:
                    logger.info(f"Already processed: {channel}/{message.id}")
                    continue
                config.channels[channel] = message.id
                post_text = message.message or ""
                logger.info(f"New: {channel}/{message.id}: {post_text[:50]}...")
                filters = await filter_match(post_text)
                for i in range(len(filters)):
                    if int(filters[i]) >= config.filter_strength:
                        for user_id in config.subscribers:
                            try:
                                await bot.send_message(
                                    chat_id=user_id,
                                    text=f"!!! {filters[i]}/{config.filter_strength}/5 \nBy: '{i}'\nlink: {channel}/{message.id}"
                                )
                            except Exception as e:
                                logger.error(f"Error sending message to {user_id}: {e}")
            except Exception as e:
                logger.error(f"Error processing channel {channel}: {e}")
        await asyncio.sleep(TELETHON_POLLING_INTERVAL)
