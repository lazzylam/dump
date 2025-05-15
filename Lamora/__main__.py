from telethon import TelegramClient
from lamora.config import api_id, api_hash, bot_token
from handlers import com

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
commands.register(client)

print("Bot berjalan...")
client.run_until_disconnected()