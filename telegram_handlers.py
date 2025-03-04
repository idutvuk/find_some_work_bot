import logging
from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from variables import Variables
from config import ADMIN_IDS
from aiogram.types import ReactionTypeEmoji
from telethon_polling import poll_for_jobs

logger = logging.getLogger(__name__)
vars = Variables()

router = Router()


class Admin:
    def __call__(self, message):
        return message.from_user.id in ADMIN_IDS

        
class NotAdmin:
    def __call__(self, message):
        return message.from_user.id not in ADMIN_IDS



@vars.use_var
@router.message(Command("subscribe"))
async def subscribe_handler(message: types.Message):
    user_id = message.from_user.id
    vars.subscribers.add(user_id)
    await message.answer(
        "You have been subscribed to job offers. If you don't want to, use /unsubscribe"
    )


@vars.use_var
@router.message(Command("unsubscribe"))
async def unsubscribe_handler(message: types.Message):
    user_id = message.from_user.id
    vars.subscribers.discard(user_id)
    await message.answer("You have been unsubscribed.")


@vars.use_var
@router.message(Admin(), Command("listsubs"))
async def user_list(message: types.Message):
    await message.answer("subs\n" + "\n".join(map(str, vars.subscribers)))


# region folder mode


@vars.use_var
@router.message(Admin(), Command("parsemode"))
async def set_parse_mode(message: types.Message):
    args = message.text.split()[1:]
    if args[0] in ["folder", "list"]:
        vars.parse_mode = args[0]
        vars.save_variables()
        await message.react(reaction=[{"type": "emoji", "emoji": "👌"}])
    else:
        await message.answer("unknown type"+args+ ".\n/parsemode folder\n/parsemode list")


# endregion


@router.message(Admin(), Command("list"))
async def list_handler(message: types.Message):
    if vars.channels:
        msg = "Current channels/groups:\n" + "\n".join(vars.channels)
    else:
        msg = "No channels/groups added."
    await message.answer(msg)


# region list mode
@vars.use_var
@router.message(Admin(), Command("add"))
async def add_handler(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /add <channel_link1> <channel_link2> ...")
        return
    for channel in args:
        if channel not in vars.channels:
            vars.channels[channel] = -1
            vars.save_variables()
            await message.react(reaction=[{"type": "emoji", "emoji": "👌"}])
        else:
            await message.answer(f"Channel '{channel}' is already in the list.")


@vars.use_var
@router.message(Admin(), Command("remove"))
async def remove_handler(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /remove <channel_link1> <channel_link2> ...")
        return
    for channel in args:
        if channel in vars.channels:
            vars.channels.pop(channel)
            await message.react(reaction=[{"type": "emoji", "emoji": "👌"}])
        else:
            await message.answer(f"Channel '{channel}' not found.")
    vars.save_variables()


@vars.use_var
@router.message(Admin(), Command("filter"))
async def filter_handler(message: types.Message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer(
            f"Filter: '{vars.filters}'\nStrength {vars.filter_strength}\nTo set filter, usage: /filter <strength> <filter1> | <filter2>"
        )
        return
    try:
        vars.filter_strength = int(args[0])
        if vars.filter_strength < 1 or vars.filter_strength > 5:
            await message.answer("Filter strength must be between 1 and 5")
            return
    except ValueError:
        await message.answer("Invalid filter strength")
        return
    vars.filters = " ".join(args[1:]).split(" | ")
    await message.react(reaction=[{"type": "emoji", "emoji": "👌"}])
    


# endregion

# region meta


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome!")
    await subscribe_handler(message)


@router.message(Command("ping"))
async def ping(message: types.Message):
    await message.react(reaction=[{"type": "emoji", "emoji": "🖕"}])

@router.message(NotAdmin())
async def fuck(message: types.Message):
    await message.react(reaction=[{"type": "emoji", "emoji": "🖕"}])


# endregion
