import os
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import database

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Wedding Photo Bot! 📸\n\n"
        "Just send any pictures you take here, and we'll save them to our gallery.\n"
        "Use /gallery to see some random photos others have submitted!"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    # Telegram sends multiple sizes of the photo. We take the last one (the largest).
    photo_file_id = update.message.photo[-1].file_id
    
    # Save to database
    database.save_photo(user_id, photo_file_id)
    
    await update.message.reply_text("Thanks! I've saved your photo. 🎉")

async def test_gallery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = database.get_random_photos(10)
    
    if not photos:
        await update.message.reply_text("No photos have been submitted yet. Be the first!")
        return
        
    media_group = [InputMediaPhoto(media=file_id) for file_id in photos]
    
    await update.message.reply_media_group(media=media_group)

def main():
    if not TELEGRAM_TOKEN:
        print("Please set TELEGRAM_TOKEN in the .env file.")
        return
        
    # Initialize the database
    database.init_db()
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gallery", test_gallery))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot is started!")
    app.run_polling()

if __name__ == '__main__':
    main()
