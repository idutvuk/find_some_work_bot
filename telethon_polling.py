import asyncio
import logging
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELETHON_POLLING_INTERVAL
from variables import Variables
from openai_filter import filter_match, filter_is_job_offer

logger = logging.getLogger(__name__)
vars = Variables()

telethon_client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def poll_channels(bot):
    await telethon_client.start()
    while True:
        vars.load_variables()
        if vars.parse_mode == "list":
            await poll_list(bot)
        elif vars.parse_mode == "folder":
            await poll_folder(bot)
        await asyncio.sleep(TELETHON_POLLING_INTERVAL)
        

async def poll_list(bot):
    for channel, id in vars.channels.items():
            try:
                messages = await telethon_client.get_messages(channel, limit=1)
                if not messages:
                    continue
                message = messages[0]
                last_read_id = id
                if message.id <= last_read_id:
                    logger.info(f"Already processed: {channel}/{message.id}")
                    continue
                vars.channels[channel] = message.id
                vars.save_variables()
                post_text = message.message or ""
                if not post_text:
                    continue
                logger.info(f"New: {channel}/{message.id}: {post_text[:50]}...")
                
                
                if not await filter_is_job_offer(post_text):
                    return

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
    
        
async def poll_folder(bot):
    for channel, id in vars.channels.items():
            try:
                messages = await telethon_client.get_messages(channel, limit=1)
                if not messages:
                    continue
                message = messages[0]
                last_read_id = id
                if message.id <= last_read_id:
                    logger.info(f"Already processed: {channel}/{message.id}")
                    continue
                vars.channels[channel] = message.id
                vars.save_variables()
                post_text = message.message or ""
                if not post_text:
                    continue
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