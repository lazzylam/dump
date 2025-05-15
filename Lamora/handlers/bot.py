from lamora.utils.tol import dev_only

def register(client):
    @client.on(events.NewMessage(pattern="/reboot"))
    @dev_only
    async def reboot_handler(event):
        msg = await event.reply("Menjalankan `git pull`...")
        result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout or result.stderr

        await msg.edit(f"```{output.strip()}```\n\nGit pull berhasil, mematikan bot...")

        # Simpan chat_id untuk notifikasi setelah restart
        with open("restart_flag.txt", "w") as f:
            f.write(str(event.chat_id))

        await asyncio.sleep(2)
        os.execv(sys.executable, [sys.executable, "-m", "lamora"])