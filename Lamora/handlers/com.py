import asyncio
import os
import subprocess
import sys
from telethon import events
from database import models as db
from utils.helpers import admin_only, extract_user_id, extract_text

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

    # Tambahkan di sini
    @client.on(events.NewMessage(pattern="/reboot"))
    @admin_only
    async def reboot_bot(event):
        msg = await event.reply("Menjalankan `git pull` untuk update...")
        result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout or result.stderr

        await msg.edit(f"```{output.strip()}```\n\nGit pull berhasil, mematikan bot...")

        # Simpan chat_id ke file agar bisa kirim notifikasi saat hidup kembali
        with open("restart_flag.txt", "w") as f:
            f.write(str(event.chat_id))

        await asyncio.sleep(2)
        os.execv(sys.executable, [sys.executable, "main.py"])  # restart proses