from telethon import TelegramClient
from lamora.config import api_id, api_hash, bot_token
from lamora.handlers import com, bot

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

com.register(client)
bot.register(client)

# Notifikasi setelah reboot
if os.path.exists("restart_flag.txt"):
    with open("restart_flag.txt", "r") as f:
        chat_id = int(f.read().strip())
    os.remove("restart_flag.txt")
    client.loop.create_task(client.send_message(chat_id, "Bot berhasil diaktifkan kembali."))

print("Bot berjalan...")
client.run_until_disconnected()