import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from config.config import TOKEN

from config.states import MAIN_MENU, SHOP, KOMBIT

from handlers.gasification_handler import terrain

from handlers.shop_handler import shop

from handlers.kommbit_handler import kommbit

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("газификация", callback_data="gasification")],
        [InlineKeyboardButton("магазин", callback_data="shop")],
        [InlineKeyboardButton("коммбыт", callback_data="kommbit")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="скоро тут будет бот для бридж сервиса...",
        reply_markup=markup,
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(terrain, pattern="^gasification$"),
                CallbackQueryHandler(shop, pattern="^shop$"),
                CallbackQueryHandler(kommbit, pattern='^kommbit$')
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)

    application.run_polling()
