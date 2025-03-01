import logging
from aiogram import Router, types
from aiogram.filters import Command
from variables import BotConfig
from config import ADMIN_IDS

logger = logging.getLogger(__name__)
config = BotConfig()

# Создаем экземпляр Router
router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome!")
    await subscribe_handler(message)

@config.use_var
@router.message(Command("subscribe"))
async def subscribe_handler(message: types.Message):
    user_id = message.from_user.id
    config.subscribers.add(user_id)
    await message.answer("You have been subscribed to job offers. If you don't want to, use /unsubscribe")

@config.use_var
@router.message(Command("unsubscribe"))
async def unsubscribe_handler(message: types.Message):
    user_id = message.from_user.id
    config.subscribers.discard(user_id)
    await message.answer("You have been unsubscribed.")

@config.use_var
@router.message(Command("add"))
async def add_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("You are not an admin.")
        return
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /add <channel_link1> <channel_link2> ...")
        return
    for channel in args:
        if channel not in config.channels:
            config.channels[channel] = -1
            config.save_variables()
            await message.answer(f"Channel '{channel}' added.")
        else:
            await message.answer(f"Channel '{channel}' is already in the list.")

@config.use_var
@router.message(Command("remove"))
async def remove_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Unauthorized")
        return
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /remove <channel_link1> <channel_link2> ...")
        return
    for channel in args:
        if channel in config.channels:
            config.channels.pop(channel)
            await message.answer(f"Channel '{channel}' removed.")
        else:
            await message.answer(f"Channel '{channel}' not found.")
    config.save_variables()

@router.message(Command("list"))
async def list_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Unauthorized")
        return
    if config.channels:
        msg = "Current channels/groups:\n" + "\n".join(config.channels)
    else:
        msg = "No channels/groups added."
    await message.answer(msg)

@config.use_var
@router.message(Command("filter"))
async def filter_handler(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Unauthorized")
        return

    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer(
            f"Filter: '{config.filter_query}'\nStrength {config.filter_strength}\nTo set filter, usage: /filter <strength> <filter>"
        )
        return
    try:
        config.filter_strength = int(args[0])
        if config.filter_strength < 1 or config.filter_strength > 5:
            await message.answer("Filter strength must be between 1 and 5")
            return
    except ValueError:
        await message.answer("Invalid filter strength")
        return
    config.filter_query = " ".join(args[1:])
    await message.answer(f"Filter updated: '{config.filter_query}'\nStrength {config.filter_strength}")
