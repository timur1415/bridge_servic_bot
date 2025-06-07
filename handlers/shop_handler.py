import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler
)

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="магаз",
    )