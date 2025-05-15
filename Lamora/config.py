from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
db_path = "aku.db"

# Developer IDs, dipisah dari admin grup, isinya user ID yang boleh akses semua command khusus
developer_ids = [int(x) for x in os.getenv("DEVELOPER_IDS", "").split(",") if x.strip().isdigit()]