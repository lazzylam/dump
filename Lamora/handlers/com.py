from telethon import events
from lamora.database import aku as db
from lamora.utils.tol import admin_only, extract_user_id, extract_text

def register(client):
    @client.on(events.NewMessage(pattern="/start"))
    async def start(event):
        await db.init_db()
        await event.reply("Bot aktif dan siap digunakan.")

    @client.on(events.NewMessage(pattern="/addbl"))
    @admin_only
    async def add_blacklist_user(event):
        uid = await extract_user_id(event)
        if uid:
            await db.add_user_blacklist(uid)
            await event.reply(f"User `{uid}` ditambahkan ke blacklist.")
        else:
            await event.reply("Format salah. Gunakan /addbl <user_id> atau reply.")

    # dst...