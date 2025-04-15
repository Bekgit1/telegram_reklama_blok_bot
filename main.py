# Main bot logic will go here
import os
import logging
from dotenv import load_dotenv
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from bot.utils import is_advertisement
from bot.locales import get_localized

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Memory-based storage
warned_users = {}
stats = {
    "deleted": 0,
    "warned": 0,
    "banned": 0
}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"
    await update.message.reply_text(get_localized(lang, "start"))

# Stats command
async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"
    text = get_localized(lang, "stats").format(**stats)
    await update.message.reply_text(text)

# Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user_id = msg.from_user.id
    chat_id = msg.chat_id
    lang = msg.from_user.language_code or "en"

    if is_advertisement(msg):
        try:
            await msg.delete()
            stats["deleted"] += 1
        except:
            return

        warned_users[user_id] = warned_users.get(user_id, 0) + 1
        warn_count = warned_users[user_id]
        stats["warned"] += 1

        if warn_count == 1:
            await msg.chat.send_message(
                f"{msg.from_user.mention_html()} {get_localized(lang, 'warn')}",
                parse_mode="HTML"
            )
        elif warn_count == 2:
            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=False)
            )
            await msg.chat.send_message(
                f"{msg.from_user.mention_html()} {get_localized(lang, 'mute')}",
                parse_mode="HTML"
            )
        elif warn_count >= 3:
            await context.bot.ban_chat_member(chat_id, user_id)
            stats["banned"] += 1
            await msg.chat.send_message(
                f"{msg.from_user.mention_html()} {get_localized(lang, 'ban')}",
                parse_mode="HTML"
            )

# Entry point
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.Document.ALL | filters.PHOTO | filters.CaptionRegex(".*"),
            handle_message
        )
    )

    app.run_polling()

if __name__ == "__main__":
    main()
