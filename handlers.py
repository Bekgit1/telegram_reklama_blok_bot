# Handlers for commands and messages
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

from bot.utils import warn_user, get_warn_count, update_stats, get_stats
from bot.filters import is_advertisement
from bot.locales import get_localized


# /start buyrug'i
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"
    await update.message.reply_text(get_localized(lang, "start"))


# /stats buyrug'i
async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"
    data = get_stats()
    text = get_localized(lang, "stats").format(**data)
    await update.message.reply_text(text)


# Reklama xabarlarini aniqlovchi asosiy handler
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = msg.from_user
    user_id = user.id
    chat_id = msg.chat_id
    lang = user.language_code or "en"

    if is_advertisement(msg):
        try:
            await msg.delete()
            update_stats("deleted")
        except:
            return  # Ehtimoliy ruxsat yo'q

        count = warn_user(user_id)
        update_stats("warned")

        if count == 1:
            await msg.chat.send_message(
                f"{user.mention_html()} {get_localized(lang, 'warn')}",
                parse_mode="HTML"
            )
        elif count == 2:
            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(can_send_messages=False)
            )
            await msg.chat.send_message(
                f"{user.mention_html()} {get_localized(lang, 'mute')}",
                parse_mode="HTML"
            )
        elif count >= 3:
            await context.bot.ban_chat_member(chat_id, user_id)
            update_stats("banned")
            await msg.chat.send_message(
                f"{user.mention_html()} {get_localized(lang, 'ban')}",
                parse_mode="HTML"
            )
