import asyncio
from lamora.config import developer_ids  # list of user_id from .env

async def is_developer(event):
    return event.sender_id in developer_ids

async def is_group_admin(event):
    try:
        if event.is_group:
            p = await event.client.get_permissions(event.chat_id, event.sender_id)
            return p.is_admin
    except:
        pass
    return False

async def is_authorized(event):
    return await is_developer(event) or await is_group_admin(event)

def authorized_only(func):
    async def wrapper(event):
        if not await is_authorized(event):
            msg = await event.reply("Hanya admin atau developer yang bisa menggunakan perintah ini.")
            await asyncio.sleep(2)
            await msg.delete()
            return
        await func(event)
    return wrapper

def developer_only(func):
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
        return int(event.text.split(" ", 1)[1])
    except:
        return None

async def extract_text(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        return reply.raw_text.strip() if reply else None
    try:
        return event.text.split(" ", 1)[1].strip()
    except:
        return None