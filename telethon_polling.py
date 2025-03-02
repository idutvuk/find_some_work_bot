import asyncio
import logging
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELETHON_POLLING_INTERVAL
from variables import Variables
from openai_filter import filter_match

logger = logging.getLogger(__name__)
vars = Variables()

telethon_client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def poll_channels(bot):
    """
    Опрос каналов и групп через Telethon.
    Для каждого нового сообщения проверяется фильтр OpenAI и, если сообщение проходит фильтрацию,
    оно пересылается подписчикам через aiogram Bot.
    """
    await telethon_client.start()
    while True:
        vars.load_variables()
        for channel in vars.channels.keys():
            try:
                messages = await telethon_client.get_messages(channel, limit=1)
                if not messages:
                    continue
                message = messages[0]
                last_id = vars.channels.get(channel, 0)
                if message.id <= last_id:
                    logger.info(f"Already processed: {channel}/{message.id}")
                    continue
                vars.channels[channel] = message.id
                post_text = message.message or ""
                logger.info(f"New: {channel}/{message.id}: {post_text[:50]}...")
                response = await filter_match(post_text)
                for i in range(len(response)):
                    if int(response[i]) >= vars.filter_strength:
                        for user_id in vars.subscribers:
                            try:
                                await bot.send_message(
                                    chat_id=user_id,
                                    text=
                                    f"!!! {response[i]}/{vars.filter_strength}/5\n"
                                    f"By: '{vars.filters[i]}'\n"
                                    f"link: {channel}/{message.id}"
                                )
                            except Exception as e:
                                logger.error(f"Error sending message to {user_id}: {e}")
            except Exception as e:
                logger.error(f"Error processing channel {channel}: {e}")
        await asyncio.sleep(TELETHON_POLLING_INTERVAL)
        
