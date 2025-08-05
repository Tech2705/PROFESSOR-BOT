from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant

# List of channel/group IDs to force subscribe. Start with one, add more by comma separating.
FORCE_SUB_CHANNELS = [-1002544936859]

# Optional: Admins who can bypass force subscribe
ADMINS = [1876329759]  # Put your Telegram user ID(s) here

async def check_sub(client: Client, user_id: int):
    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False, channel
        except UserNotParticipant:
            return False, channel
        except Exception:
            return False, channel
    return True, None

@Client.on_message(filters.private & ~filters.command("start"))
async def force_sub_handler(client, message: Message):
    if message.from_user.id in ADMINS:
        return
    is_joined, channel = await check_sub(client, message.from_user.id)
    if not is_joined:
        try:
            invite_link = await client.create_chat_invite_link(channel)
            link = invite_link.invite_link
        except Exception:
            link = f"https://t.me/c/{str(channel)[4:]}"  # Fallback
        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Channel", url=link)]]
        )
        await message.reply(
            "You must join our channel to use this bot.",
            reply_markup=btn,
        )
        return
