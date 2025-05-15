import asyncio

async def is_group_admin(event):
    if not event.is_group:
        return False

    try:
        perms = await event.client.get_permissions(event.chat_id, event.sender_id)
        return perms.is_admin or perms.is_creator
    except:
        return False

def admin_only(func):
    async def wrapper(event):
        if not await is_group_admin(event):
            msg = await event.reply("Perintah ini hanya untuk admin grup.")
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