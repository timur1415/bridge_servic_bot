import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from config.states import SHOP


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("МОНТАЖНИКАМ", callback_data="fitter")],
        [InlineKeyboardButton("Бридж-Маркет", callback_data="market")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/main_shop.jpg", "rb"),
        reply_markup=markup,
    )
    return SHOP
