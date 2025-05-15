from telethon import events
from Lamora.database import aku as db
from Lamora.utils.tol import admin_only, extract_user_id, extract_text

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

    @client.on(events.NewMessage(pattern="/bl"))
    @admin_only
    async def add_blacklist_word(event):
        word = await extract_text(event)
        if word:
            await db.add_word_blacklist(word)
            await event.reply(f"Kata `{word}` ditambahkan ke blacklist.")
        else:
            await event.reply("Format salah. Gunakan /bl <kata> atau reply.")

    @client.on(events.NewMessage(pattern="/listbl"))
    @admin_only
    async def list_blacklist(event):
        users = await db.list_blacklist_users()
        words = await db.list_blacklist_words()
        user_list = "\n".join(str(u[0]) for u in users) or "Kosong"
        word_list = "\n".join(w[0] for w in words) or "Kosong"
        await event.reply(f"**Blacklist Users:**\n{user_list}\n\n**Blacklist Words:**\n{word_list}")

    @client.on(events.NewMessage(pattern="/clearbl"))
    @admin_only
    async def clear_blacklist(event):
        await db.clear_blacklist()
        await event.reply("Seluruh data blacklist telah dihapus.")