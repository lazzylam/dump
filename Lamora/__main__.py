from telethon import TelegramClient
from lamora.config import api_id, api_hash, bot_token
from lamora.handlers import com, reboot  # Tambahkan modul reboot jika ada

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Daftarkan semua command handler
com.register(client)
reboot.register(client)  # Tambahkan ini jika kamu sudah pisahkan /reboot

print("Bot berjalan...")
client.run_until_disconnected()