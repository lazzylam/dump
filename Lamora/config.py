from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
db_path = "aku.db"
admin_ids = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]