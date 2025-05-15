from telethon import events
from Lamora.database import aku as db
from Lamora.utils.tol import admin_only, extract_user_id, extract_text

def register(client):
    @client.on(events.NewMessage(pattern="/addwhite"))
    @admin_only
    async def add_whitelist_user(event):
        uid = await extract_user_id(event)
        if uid:
            await db.add_user_whitelist(uid)
            await event.reply(f"User `{uid}` berhasil ditambahkan ke whitelist.")
        else:
            await event.reply("Format salah. Gunakan /addwhite <user_id> atau balas pesan user.")

    @client.on(events.NewMessage(pattern="/white"))
    @admin_only
    async def add_whitelist_word(event):
        word = await extract_text(event)
        if word:
            await db.add_word_whitelist(word)
            await event.reply(f"Kata `{word}` berhasil ditambahkan ke whitelist.")
        else:
            await event.reply("Format salah. Gunakan /white <kata> atau balas pesan.")

    @client.on(events.NewMessage(pattern="/listwhite"))
    @admin_only
    async def list_whitelist(event):
        users = await db.list_whitelist_users()
        words = await db.list_whitelist_words()
        user_list = "\n".join(str(u[0]) for u in users) or "Kosong"
        word_list = "\n".join(w[0] for w in words) or "Kosong"
        await event.reply(f"**Whitelist Users:**\n{user_list}\n\n**Whitelist Words:**\n{word_list}")

    @client.on(events.NewMessage(pattern="/clearwhite"))
    @admin_only
    async def clear_whitelist(event):
        await db.clear_whitelist()
        await event.reply("Whitelist users dan words sudah dikosongkan.")