import asyncio
from telethon import events
from database import db as db_funcs

def register(client):

    @client.on(events.NewMessage(pattern="/start"))
    async def start_handler(event):
        await db_funcs.init_db()
        await event.reply("Bot siap digunakan.")

    @client.on(events.NewMessage(pattern="/addbl"))
    async def add_blacklist_user(event):
        uid = await extract_user_id(event)
        if uid:
            await db_funcs.add_entry("blacklist_users", uid)
            await event.reply(f"User {uid} ditambahkan ke blacklist.")

    @client.on(events.NewMessage(pattern="/addwhite"))
    async def add_whitelist_user(event):
        uid = await extract_user_id(event)
        if uid:
            await db_funcs.add_entry("whitelist_users", uid)
            await event.reply(f"User {uid} ditambahkan ke whitelist.")

    @client.on(events.NewMessage(pattern="/bl"))
    async def add_blacklist_word(event):
        word = await extract_text(event)
        if word:
            await db_funcs.add_entry("blacklist_words", word)
            await event.reply(f"Kata '{word}' ditambahkan ke blacklist.")

    @client.on(events.NewMessage(pattern="/white"))
    async def add_whitelist_word(event):
        word = await extract_text(event)
        if word:
            await db_funcs.add_entry("whitelist_words", word)
            await event.reply(f"Kata '{word}' ditambahkan ke whitelist.")

    @client.on(events.NewMessage(pattern="/listbl"))
    async def list_blacklist(event):
        users = await db_funcs.list_entries("blacklist_users")
        words = await db_funcs.list_entries("blacklist_words")
        await event.reply(f"**Blacklist Users:**\n{users}\n\n**Blacklist Words:**\n{words}")

    @client.on(events.NewMessage(pattern="/listwhite"))
    async def list_whitelist(event):
        users = await db_funcs.list_entries("whitelist_users")
        words = await db_funcs.list_entries("whitelist_words")
        await event.reply(f"**Whitelist Users:**\n{users}\n\n**Whitelist Words:**\n{words}")

    @client.on(events.NewMessage(pattern="/clearbl"))
    async def clear_blacklist(event):
        await db_funcs.clear_table("blacklist_users")
        await db_funcs.clear_table("blacklist_words")
        await event.reply("Blacklist dibersihkan.")

    @client.on(events.NewMessage(pattern="/clearwhite"))
    async def clear_whitelist(event):
        await db_funcs.clear_table("whitelist_users")
        await db_funcs.clear_table("whitelist_words")
        await event.reply("Whitelist dibersihkan.")

# Helpers
async def extract_user_id(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        return msg.sender_id
    try:
        return int(event.text.split(" ", 1)[1])
    except:
        await event.reply("Format salah. Gunakan /addbl <user_id> atau reply.")
        return None

async def extract_text(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        return msg.raw_text.strip()
    try:
        return event.text.split(" ", 1)[1].strip()
    except:
        await event.reply("Format salah. Gunakan /bl <kata> atau reply.")
        return None
