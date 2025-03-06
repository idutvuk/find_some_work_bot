import asyncio
import logging
from telethon import TelegramClient, functions

from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELETHON_POLLING_INTERVAL
from variables import Variables
from openai_filter import filter_match, filter_is_job_offer

logger = logging.getLogger(__name__)
vars = Variables()

telethon_client = TelegramClient("session_name", TELEGRAM_API_ID, TELEGRAM_API_HASH)


async def poll_for_jobs(bot):
    """calls poll_channels() with folder xor list"""
    await telethon_client.start()
    while True:
        vars.load_variables()
        if vars.parse_mode == "list":
            await poll_channels(bot, vars.channels.items())
            # await poll_channels(bot, vars.channels.items())
        elif vars.parse_mode == "folder":  # todo implement
            res = await telethon_client(functions.messages.GetDialogFiltersRequest())
            channel_ids = [
                peer.channel_id
                for filter in res.filters
                if hasattr(filter, "include_peers")
                for peer in filter.include_peers
                if hasattr(peer, "channel_id")
            ]
            await poll_channels(bot, list(zip(channel_ids, [-1] * len(channel_ids))))

        await asyncio.sleep(TELETHON_POLLING_INTERVAL)


async def poll_channels(bot, items: list[tuple]):
    new_count, offers_count, passed_offers_count = 0, 0, 0
    logger.info(f"Polling {len(items)} items")
    for channel, id in items:
        try:
            messages = await telethon_client.get_messages(channel, limit=1)
            if not messages:
                continue
            message = messages[0]
            if message.id <= id:
                continue
            vars.channels[channel] = message.id
            if vars.parse_mode == "list":
                vars.save_variables()
            post_text = message.message or ""
            if not post_text:
                continue
            logger.info(f"New: {channel}/{message.id}: {post_text[:50]}...")
            new_count += 1
            if not await filter_is_job_offer(post_text):
                continue
            offers_count += 1

            response = await filter_match(post_text)
            for i in range(len(response)):
                if int(response[i]) >= vars.filter_strength:  # if filter passes
                    passed_offers_count += 1
                    for user_id in vars.subscribers:
                        try:
                            await bot.send_message(
                                chat_id=user_id,
                                text=f"!!! {response[i]}/5 (passed {vars.filter_strength}/5 filter)\n{vars.filters[i]}\nlink: {channel}/{message.id}",
                                disable_web_page_preview=vars.post_preview
                            )
                        except Exception as e:
                            logger.error(f"Error sending message to {user_id}: {e}")
                    break # todo remove if individual filters
        except Exception as e:
            logger.error(f"Error processing channel {channel}: {e}")
    logger.info(
        f"Polled ({passed_offers_count} related job) / ({offers_count} job) / ({new_count} new) / ({len(items)} items)"
    )
