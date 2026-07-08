import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    try:
        ydl_opts = {
            "outtmpl": "downloads/%(title)s.%(ext)s"
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_text("Uploading...")

        with open(filename, "rb") as f:
            await context.bot.send_document(
                chat_id=CHANNEL_ID,
                document=f
            )

        os.remove(filename)

        await update.message.reply_text("✅ Done!")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot is running...")
app.run_polling()
