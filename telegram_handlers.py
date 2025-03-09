import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import ReactionTypeEmoji

from variables import Variables
from config import ADMIN_IDS

logger = logging.getLogger(__name__)
v = Variables()

router = Router()


class Admin:
    def __call__(self, message):
        return message.from_user.id in ADMIN_IDS


class NotAdmin:
    def __call__(self, message):
        return message.from_user.id not in ADMIN_IDS


@router.message(Command("subscribe"))
async def subscribe_handler(message: types.Message):
    v.subscribers.add(message.chat.id)
    await message.answer(
        "You have been subscribed to job offers. If you don't want to, use /unsubscribe"
    )
    v.save_variables()


@router.message(Command("unsubscribe"))
async def unsubscribe_handler(message: types.Message):
    user_id = message.chat.id
    v.subscribers.discard(user_id)
    await message.answer("You have been unsubscribed.")
    v.save_variables()


@router.message(Admin(), Command("subs"))
async def user_list(message: types.Message):
    await message.answer("subs\n" + "\n".join(map(str, v.subscribers)))


# region folder mode


@router.message(Admin(), Command("parsemode"))
async def set_parse_mode(message: types.Message):
    args = message.text.split()[1:]
    if args[0] in ["folder", "list"]:
        v.parse_mode = args[0]
        v.save_variables()
        await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])
    else:
        await message.answer(
            "unknown type" + str(args) + ".\n/parsemode folder\n/parsemode list"
        )


# endregion


@router.message(Admin(), Command("list"))
async def list_handler(message: types.Message):
    if v.channels:
        msg = f"Total {len(v.channels)} chats:" + "\n" + "\n".join(v.channels)
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
        if channel not in v.channels:
            v.channels[channel] = -1
            v.save_variables()
            await message.react(reaction=[ReactionTypeEmoji( emoji="👌")])
        else:
            await message.answer(f"Channel '{channel}' is already in the list.")


@router.message(Admin(), Command("remove"))
async def remove_handler(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer("Usage: /remove <channel_link1> <channel_link2> ...")
        return
    for channel in args:
        if channel in v.channels:
            v.channels.pop(channel)
            # noinspection PyTypeChecker
            await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])
        else:
            await message.answer(f"Channel '{channel}' not found.")
    v.save_variables()


@router.message(Admin(), Command("filter"))
async def filter_handler(message: types.Message):
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer(
            f"Filter: {' | '.join(v.filters)}\nStrength {v.filter_strength}\nTo set filter, usage: /filter <strength> <filter1> | <filter2>"
        )
        return
    try:
        v.filter_strength = int(args[0])
        if v.filter_strength < 1 or v.filter_strength > 5:
            await message.answer("Filter strength must be between 1 and 5")
            return
    except ValueError:
        await message.answer("Invalid filter strength")
        return
    v.filters = " ".join(args[1:]).split(" | ")
    v.save_variables()
    await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])

@router.message(Admin(), Command("negative"))
async def negative_handler(message: types.Message):
    args = message.text.split()[1:]
    if len(args) < 1:
        await message.answer(
            f"Negative: {' | '.join(v.negative)}\nTo set negative prompts, usage: /negative <neg1> | <neg2>"
        )
        return
    v.negative = " ".join(args[1:]).split(" | ")
    v.save_variables()
    await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])


# endregion

# region meta


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome!")
    await subscribe_handler(message)


@router.message(Command("ping"))
async def ping(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🖕")])


@router.message(NotAdmin(), F.text.startswith("/"), ~F.text.startswith("ping"))
async def fuck(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🖕")])

# just for handling message
@router.message(~F.text.startswith("/"))
async def not_command(message: types.Message):
    pass
# endregion
