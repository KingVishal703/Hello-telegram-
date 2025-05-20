import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # e.g. @yourchannel or -100...

video_ids = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started! Use /getvideo to get a random video.")

async def getvideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not video_ids:
        await update.message.reply_text("No videos found in channel.")
        return
    video_id = random.choice(video_ids)
    await context.bot.send_video(chat_id=update.effective_chat.id, video=video_id)

async def fetch_channel_videos(app):
    print("Fetching videos from channel...")
    async for message in app.bot.get_chat(CHANNEL_USERNAME).iter_history():
        if message.video:
            video_ids.append(message.video.file_id)
    print(f"Fetched {len(video_ids)} videos.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getvideo", getvideo))

    await fetch_channel_videos(app)
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
