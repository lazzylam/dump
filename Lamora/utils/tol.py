import asyncio
from Lamora.config import developer_ids

async def is_developer(event):
    return event.sender_id in developer_ids

async def is_group_admin(event):
    if not event.is_group:
        return False
    chat = await event.get_chat()
    participant = await event.client.get_participant(chat.id, event.sender_id)
    return participant.is_admin or participant.is_creator

def admin_only(func):
    async def wrapper(event):
        if not (await is_developer(event) or await is_group_admin(event)):
            msg = await event.reply("Hanya admin grup atau developer yang bisa menggunakan perintah ini.")
            await asyncio.sleep(2)
            await msg.delete()
            return
        await func(event)
    return wrapper

def dev_only(func):
    async def wrapper(event):
        if not await is_developer(event):
            msg = await event.reply("Hanya developer yang bisa menggunakan perintah ini.")
            await asyncio.sleep(2)
            await msg.delete()
            return
        await func(event)
    return wrapper

async def extract_user_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        return reply.sender_id if reply else None
    try:
        parts = event.text.split(" ", 1)
        if len(parts) > 1:
            return int(parts[1])
    except Exception:
        return None

async def extract_text(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        return reply.raw_text.strip() if reply else None
    try:
        parts = event.text.split(" ", 1)
        if len(parts) > 1:
            return parts[1].strip()
    except Exception:
        return None