async def extract_user_id(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        return msg.sender_id
    try:
        return int(event.text.split(" ", 1)[1])
    except:
        await event.reply("Gunakan /addbl <user_id> atau reply.")
        return None

async def extract_text(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        return msg.raw_text.strip()
    try:
        return event.text.split(" ", 1)[1].strip()
    except:
        await event.reply("Gunakan /bl <kata> atau reply.")
        return None
