import asyncio
from lamora.config import admin_ids  # disesuaikan sesuai struktur folder

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