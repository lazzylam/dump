from telethon import events
from database import models as db
from utils.helpers import extract_user_id, extract_text

def register(client):

    @client.on(events.NewMessage(pattern="/start"))
    async def start(event):
        await db.init_db()
        await event.reply("Bot siap digunakan.")

    @client.on(events.NewMessage(pattern="/addbl"))
    async def add_blacklist_user(event):
        uid = await extract_user_id(event)
        if uid:
            await db.db_execute("INSERT OR IGNORE INTO blacklist_users VALUES (?)", (uid,))
            await event.reply(f"User {uid} ditambahkan ke blacklist.")

    @client.on(events.NewMessage(pattern="/bl"))
    async def add_blacklist_word(event):
        word = await extract_text(event)
        if word:
            await db.db_execute("INSERT OR IGNORE INTO blacklist_words VALUES (?)", (word,))
            await event.reply(f"Kata '{word}' ditambahkan ke blacklist.")

    @client.on(events.NewMessage(pattern="/listbl"))
    async def list_blacklist(event):
        users = await db.db_fetch_all("SELECT * FROM blacklist_users")
        words = await db.db_fetch_all("SELECT * FROM blacklist_words")
        await event.reply(f"Blacklist Users:\n{[u[0] for u in users]}\n\nWords:\n{[w[0] for w in words]}")

    @client.on(events.NewMessage(pattern="/clearbl"))
    async def clear_blacklist(event):
        await db.db_execute("DELETE FROM blacklist_users")
        await db.db_execute("DELETE FROM blacklist_words")
        await event.reply("Blacklist dibersihkan.")
