async def init_db():
    async with aiosqlite.connect(db_path) as db:
        # existing blacklist tables
        await db.execute("CREATE TABLE IF NOT EXISTS blacklist_users (user_id INTEGER PRIMARY KEY)")
        await db.execute("CREATE TABLE IF NOT EXISTS blacklist_words (word TEXT PRIMARY KEY)")
        # new whitelist tables
        await db.execute("CREATE TABLE IF NOT EXISTS whitelist_users (user_id INTEGER PRIMARY KEY)")
        await db.execute("CREATE TABLE IF NOT EXISTS whitelist_words (word TEXT PRIMARY KEY)")
        await db.commit()

async def add_user_whitelist(uid: int):
    await execute_query("INSERT OR IGNORE INTO whitelist_users VALUES (?)", (uid,))

async def add_word_whitelist(word: str):
    await execute_query("INSERT OR IGNORE INTO whitelist_words VALUES (?)", (word,))

async def list_whitelist_users():
    return await fetch_all("SELECT user_id FROM whitelist_users")

async def list_whitelist_words():
    return await fetch_all("SELECT word FROM whitelist_words")

async def clear_whitelist():
    await execute_query("DELETE FROM whitelist_users")
    await execute_query("DELETE FROM whitelist_words")