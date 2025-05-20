import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Use "-100xxxxxxxxxx" format

video_ids = []

async def fetch_channel_videos(app):
    global video_ids
    print("Fetching video file_ids from channel...")
    updates = await app.bot.get_chat(CHANNEL_USERNAME)
    async for msg in app.bot.get_chat_history(CHANNEL_USERNAME, limit=100):
        if msg.video:
            video_ids.append(msg.video.file_id)
    print(f"Fetched {len(video_ids)} videos.")

async def getvideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not video_ids:
        await update.message.reply_text("No videos found in channel.")
        return
    file_id = random.choice(video_ids)
    await update.message.reply_video(file_id)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("getvideo", getvideo))
    await fetch_channel_videos(app)
    print("Bot started.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
