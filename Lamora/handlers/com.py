import asyncio
from telethon import events
from database import db, save_db

def register(client):
    async def is_admin(event):
        if event.is_private:
            return True
        try:
            participant = await client.get_participant(event.chat_id, event.sender_id)
            return participant.participant.admin_rights or participant.participant.rank
        except:
            return False

    async def check_access(event):
        if event.is_private:
            return True
        if not await is_admin(event):
            msg = await event.reply("Hanya admin yang bisa menggunakan perintah ini.")
            await asyncio.sleep(2)
            await msg.delete()
            return False
        return True

    def group_only(func):
        async def wrapper(event):
            if event.is_private:
                msg = await event.reply("Perintah ini hanya dapat digunakan di grup.")
                await asyncio.sleep(2)
                await msg.delete()
                return
            if await check_access(event):
                await func(event)
        return wrapper

    @client.on(events.NewMessage(pattern="/addbl"))
    @group_only
    async def add_blacklist_user(event):
        reply = await event.get_reply_message()
        if reply:
            uid = reply.sender_id
        else:
            try:
                uid = int(event.raw_text.split(" ", 1)[1])
            except:
                msg = await event.reply("Format salah. Gunakan /addbl <user_id> atau reply.")
                await asyncio.sleep(2)
                await msg.delete()
                return
        if uid not in db.blacklist_users:
            db.blacklist_users.append(uid)
            save_db()
            msg = await event.reply(f"User `{uid}` ditambahkan ke blacklist.")
            await asyncio.sleep(2)
            await msg.delete()

    @client.on(events.NewMessage(pattern="/addwhite"))
    @group_only
    async def add_whitelist_user(event):
        reply = await event.get_reply_message()
        if reply:
            uid = reply.sender_id
        else:
            try:
                uid = int(event.raw_text.split(" ", 1)[1])
            except:
                msg = await event.reply("Format salah. Gunakan /addwhite <user_id> atau reply.")
                await asyncio.sleep(2)
                await msg.delete()
                return
        if uid not in db.whitelist_users:
            db.whitelist_users.append(uid)
            save_db()
            msg = await event.reply(f"User `{uid}` ditambahkan ke whitelist.")
            await asyncio.sleep(2)
            await msg.delete()

    @client.on(events.NewMessage(pattern="/bl"))
    @group_only
    async def add_blacklist_word(event):
        reply = await event.get_reply_message()
        if reply:
            word = reply.raw_text
        else:
            try:
                word = event.raw_text.split(" ", 1)[1]
            except:
                msg = await event.reply("Format salah. Gunakan /bl <kata> atau reply.")
                await asyncio.sleep(2)
                await msg.delete()
                return
        if word not in db.blacklist_words:
            db.blacklist_words.append(word)
            save_db()
            msg = await event.reply(f"Kata `{word}` ditambahkan ke blacklist.")
            await asyncio.sleep(2)
            await msg.delete()

    @client.on(events.NewMessage(pattern="/white"))
    @group_only
    async def add_whitelist_word(event):
        reply = await event.get_reply_message()
        if reply:
            word = reply.raw_text
        else:
            try:
                word = event.raw_text.split(" ", 1)[1]
            except:
                msg = await event.reply("Format salah. Gunakan /white <kata> atau reply.")
                await asyncio.sleep(2)
                await msg.delete()
                return
        if word not in db.whitelist_words:
            db.whitelist_words.append(word)
            save_db()
            msg = await event.reply(f"Kata `{word}` ditambahkan ke whitelist.")
            await asyncio.sleep(2)
            await msg.delete()

    @client.on(events.NewMessage(pattern="/delbltext"))
    @group_only
    async def delete_blacklist_word(event):
        try:
            word = event.raw_text.split(" ", 1)[1]
        except:
            msg = await event.reply("Format salah. Gunakan /delbltext <kata>")
            await asyncio.sleep(2)
            await msg.delete()
            return
        if word in db.blacklist_words:
            db.blacklist_words.remove(word)
            save_db()
            msg = await event.reply(f"Kata `{word}` dihapus dari blacklist.")
        else:
            msg = await event.reply(f"Kata `{word}` tidak ditemukan di blacklist.")
        await asyncio.sleep(2)
        await msg.delete()

    @client.on(events.NewMessage(pattern="/delwhite"))
    @group_only
    async def delete_whitelist_word(event):
        try:
            word = event.raw_text.split(" ", 1)[1]
        except:
            msg = await event.reply("Format salah. Gunakan /delwhite <kata>")
            await asyncio.sleep(2)
            await msg.delete()
            return
        if word in db.whitelist_words:
            db.whitelist_words.remove(word)
            save_db()
            msg = await event.reply(f"Kata `{word}` dihapus dari whitelist.")
        else:
            msg = await event.reply(f"Kata `{word}` tidak ditemukan di whitelist.")
        await asyncio.sleep(2)
        await msg.delete()

    @client.on(events.NewMessage(pattern="/deluser"))
    @group_only
    async def delete_user_from_lists(event):
        try:
            uid = int(event.raw_text.split(" ", 1)[1])
        except:
            msg = await event.reply("Format salah. Gunakan /deluser <user_id>")
            await asyncio.sleep(2)
            await msg.delete()
            return

        removed = []
        if uid in db.blacklist_users:
            db.blacklist_users.remove(uid)
            removed.append("blacklist")
        if uid in db.whitelist_users:
            db.whitelist_users.remove(uid)
            removed.append("whitelist")

        if removed:
            save_db()
            msg = await event.reply(f"User `{uid}` dihapus dari: {', '.join(removed)}.")
        else:
            msg = await event.reply(f"User `{uid}` tidak ada di blacklist/whitelist.")
        await asyncio.sleep(2)
        await msg.delete()

    @client.on(events.NewMessage(pattern="/listbl"))
    @group_only
    async def list_blacklist(event):
        users = "\n".join(str(u) for u in db.blacklist_users) or "Kosong"
        words = "\n".join(db.blacklist_words) or "Kosong"
        await event.reply(f"**Blacklist Users:**\n{users}\n\n**Blacklist Words:**\n{words}")

    @client.on(events.NewMessage(pattern="/listwhite"))
    @group_only
    async def list_whitelist(event):
        users = "\n".join(str(u) for u in db.whitelist_users) or "Kosong"
        words = "\n".join(db.whitelist_words) or "Kosong"
        await event.reply(f"**Whitelist Users:**\n{users}\n\n**Whitelist Words:**\n{words}")

    @client.on(events.NewMessage(pattern="/clearbl"))
    @group_only
    async def clear_blacklist(event):
        db.blacklist_users.clear()
        db.blacklist_words.clear()
        save_db()
        msg = await event.reply("Seluruh blacklist users dan kata telah dihapus.")
        await asyncio.sleep(2)
        await msg.delete()

    @client.on(events.NewMessage(pattern="/clearwhite"))
    @group_only
    async def clear_whitelist(event):
        db.whitelist_users.clear()
        db.whitelist_words.clear()
        save_db()
        msg = await event.reply("Seluruh whitelist users dan kata telah dihapus.")
        await asyncio.sleep(2)
        await msg.delete()



    @client.on(events.NewMessage(pattern="/reload"))
    @group_only
    async def reload_command(event):
        msg = await event.reply("Reloading konfigurasi database...")
        try:
            import importlib
            import database
            importlib.reload(database)
            globals()["db"] = database.db
            globals()["save_db"] = database.save_db
            await msg.edit("Reload sukses!")
        except Exception as e:
            await msg.edit(f"Reload gagal: {e}")
        await asyncio.sleep(2)
        await msg.delete()