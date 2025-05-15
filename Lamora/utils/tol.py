import asyncio
from config import admin_ids

async def is_admin(event):
    return event.sender_id in admin_ids

def admin_only(func):
    async def wrapper(event):
        if not await is_admin(event):
            msg = await event.reply("Hanya admin yang bisa menggunakan perintah ini.")
            await asyncio.sleep(2)
            await msg.delete()
            return
        await func(event)
    return wrapper

async def extract_user_id(event):
    if event.is_reply:
        return (await event.get_reply_message()).sender_id
    try:
        return int(event.text.split(" ", 1)[1])
    except:
        return None

async def extract_text(event):
    if event.is_reply:
        return (await event.get_reply_message()).raw_text.strip()
    try:
        return event.text.split(" ", 1)[1].strip()
    except:
        return None