import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    PicklePersistence
)

from config.config import TOKEN

from config.states import (
    TERRAIN,
    MAIN_MENU,
    SHOP,
    BUSINESS,
    GAS_START,
    WHEN,
    PROJECT,
    ROOM,
    METRE,
    FACADE,
    PRESSURE,
    DOCUMENTS,
    APPS,
    NAME,
    NUMBER,
    FINISH,
)

from handlers.gasification_handler import (
    terrain,
    when,
    project,
    room,
    metre,
    fasade,
    pressure,
    documents,
    apps,
    name,
    number,
    finish,
    gas_start
)

from handlers.shop_handler import shop

from handlers.business_handler import business

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message = await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="извините",
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    # await context.bot.delete_message(
    #     chat_id=update.effective_chat.id, message_id=message.id
    # )
    keyboard = [
        [InlineKeyboardButton("газификация", callback_data="gasification")],
        [InlineKeyboardButton("магазин", callback_data="shop")],
        [InlineKeyboardButton("газификация бизнеса", callback_data="business")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/main.jpg", "rb"),
        reply_markup=(markup),
    )

    return MAIN_MENU


if __name__ == "__main__":
    persistence = PicklePersistence(filepath='bridge_bot')
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(gas_start, pattern="^gasification$"),
                CallbackQueryHandler(shop, pattern="^shop$"),
                CallbackQueryHandler(business, pattern="^business$"),
            ],
            GAS_START:[MessageHandler(filters.TEXT & ~filters.COMMAND, gas_start),
                CallbackQueryHandler(terrain, pattern="^start_gas$"),
                CallbackQueryHandler(start, pattern="^back$"),],
            TERRAIN:[MessageHandler(filters.TEXT & ~filters.COMMAND, terrain)],
            WHEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, when)],
            PROJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, project)],
            ROOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, room)],
            METRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, metre)],
            FACADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, fasade)],
            PRESSURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, pressure)],
            DOCUMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, documents)],
            APPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, apps)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
            FINISH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish),
                CallbackQueryHandler(start, pattern="^main_menu$"),
            ],
        },
        name='bridge_bot',
        persistent=True,
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
