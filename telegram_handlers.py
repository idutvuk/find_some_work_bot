import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from variables import Variables
from config import ADMIN_IDS

logger = logging.getLogger(__name__)
vars = Variables()

router = Router()


class Admin:
    def __call__(self, message):
        return message.from_user.id in ADMIN_IDS


class NotAdmin:
    def __call__(self, message):
        return message.from_user.id not in ADMIN_IDS


@router.message(Command("subscribe"))
async def subscribe_handler(message: types.Message):
    vars.subscribers.add(message.chat.id)
    await message.answer(
        "You have been subscribed to job offers. If you don't want to, use /unsubscribe"
    )
    vars.save_variables()


@router.message(Command("unsubscribe"))
async def unsubscribe_handler(message: types.Message):
    user_id = message.chat.id
    vars.subscribers.discard(user_id)
    await message.answer("You have been unsubscribed.")
    vars.save_variables()


@router.message(Admin(), Command("listsubs"))
async def user_list(message: types.Message):
    await message.answer("subs\n" + "\n".join(map(str, vars.subscribers)))


# region folder mode


@router.message(Admin(), Command("parsemode"))
async def set_parse_mode(message: types.Message):
    args = message.text.split()[1:]
    if args[0] in ["folder", "list"]:
        vars.parse_mode = args[0]
        vars.save_variables()
        await message.react(reaction=[{"type": "emoji", "emoji": "👌"}])
    else:
        await message.answer(
            "unknown type" + args + ".\n/parsemode folder\n/parsemode list"
        )


# endregion


@router.message(Admin(), Command("list"))
async def list_handler(message: types.Message):
    if vars.channels:
        msg = f"Total {len(vars.channels)} chats:" + "\n" + "\n".join(vars.channels)
    else:
        msg = "No channels/groups added."
    await message.answer(msg)


# region list mode
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


@router.message(Admin(), Command("filter"))
async def filter_handler(message: types.Message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer(
            f"Filter: {' | '.join(vars.filters)}\nStrength {vars.filter_strength}\nTo set filter, usage: /filter <strength> <filter1> | <filter2>"
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
    vars.save_variables()
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


@router.message(NotAdmin(), F.text.startswith("/"), ~F.text.startswith("ping"))
async def fuck(message: types.Message):
    await message.react(reaction=[{"type": "emoji", "emoji": "🖕"}])

# just for handling message
@router.message(~F.text.startswith("/"))
async def not_command(message: types.Message):
    pass
# endregion
