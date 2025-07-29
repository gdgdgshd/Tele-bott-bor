import requests, random, string, asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8436110167:AAG1t9tezYYe7_N5Xx9kuWA1fVazK066eyY"
ALLOWED_ID = "7833885254"
scanning = False

async def scan_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global scanning
    if str(update.effective_user.id) != ALLOWED_ID:
        return
    if scanning:
        await update.message.reply_text("Already scanning...")
        return
    scanning = True
    await update.message.reply_text("Started infinite TikTok username scan...")
    while scanning:
        username = random.choice(string.ascii_lowercase) + ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(2))
        url = f"https://www.tiktok.com/@{username}"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        if "profile-error" in r.text or r.status_code == 404:
            await update.message.reply_text(f"{username} ✅")
        else:
            await update.message.reply_text(f"{username} 🚫")
        await asyncio.sleep(1)

async def stop_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global scanning
    if str(update.effective_user.id) != ALLOWED_ID:
        return
    scanning = False
    await update.message.reply_text("Stopped scanning.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", scan_tiktok))
    app.add_handler(CommandHandler("stop", stop_scan))
    app.run_polling()

if __name__ == "__main__":
    main()