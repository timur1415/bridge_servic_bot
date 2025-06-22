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
    PicklePersistence,
)

from config.config import TOKEN

from config.states import (
    MAIN_MENU,
    SHOP,
    BUSINESS,
    AGREED_GAS,
    AGREED_MOUNTER,
    GAS_START,
    TERRAIN,
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
    MOUNTER,
    FINISH,
    NUMBER_MOUNTER,
    COMMENT,
    FINISH_AMOUNTER,
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
    gas_start,
    agreed_gas,
)

from handlers.mounter import (
    fitter,
    agreeds_mounter,
    name_mounter,
    number_mounter,
    comment_mounter,
    finish_amounter,
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
        reply_markup=markup,
    )

    return MAIN_MENU


if __name__ == "__main__":
    persistence = PicklePersistence(filepath="bridge_bot")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(agreed_gas, pattern="^gasification$"),
                CallbackQueryHandler(shop, pattern="^shop$"),
                CallbackQueryHandler(business, pattern="^business$"),
            ],
            SHOP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, shop),
                CallbackQueryHandler(fitter, pattern="^fitter$"),
                CallbackQueryHandler(start, pattern="^market$"),
            ],
            AGREED_MOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, agreeds_mounter),
                CallbackQueryHandler(name_mounter, pattern="^agreed_mounter$"),
                CallbackQueryHandler(start, pattern="^no_agreed_mounter$"),
            ],
            MOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, fitter),
                CallbackQueryHandler(agreeds_mounter, pattern="^leave$"),
            ],
            AGREED_GAS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, agreed_gas),
                CallbackQueryHandler(gas_start, pattern="^agreed$"),
                CallbackQueryHandler(start, pattern="^no_agreed$"),
            ],
            GAS_START: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, gas_start),
                CallbackQueryHandler(terrain, pattern="^start_gas$"),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            TERRAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, terrain)],
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
            NUMBER_MOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, number_mounter)
            ],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comment_mounter)],
            FINISH_AMOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish_amounter)
            ],
        },
        name="bridge_bot",
        persistent=True,
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
