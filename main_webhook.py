import asyncio
import html
import logging
from dataclasses import dataclass
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request, Response, status

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
)

from config.config import URL, PORT, TOKEN

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
    AGREED_MARKET,
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
    BRIDG_MARKET,
    NAME_MARKET,
    PHONE_BUSINESS,
    AGREED_BUSINES,
    FINISH_BUSINES,
    FINISH_MARKET,
    NUMBER_MARKET,
    COMMENT_MARKET
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

from handlers.bridg_market import name_market, number_market, comment_market, finish_market

from handlers.mounter import (
    fitter,
    agreeds_mounter,
    name_mounter,
    number_mounter,
    comment_mounter,
    finish_amounter,
)

from handlers.shop_handler import shop

from handlers.business_handler import business, name_business, phone_business, finish_business, agree_business

from handlers.bridg_market import magaz, agreed_market, delivery

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message = await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="Извините",
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    # await context.bot.delete_message(
    #     chat_id=update.effective_chat.id, message_id=message.id
    # )
    keyboard = [
        [InlineKeyboardButton("Газификация", callback_data="gasification")],
        [InlineKeyboardButton("Магазин", callback_data="shop")],
        [InlineKeyboardButton("Газификация бизнеса", callback_data="business")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/main.jpg", "rb"),
        reply_markup=markup,
    )

    return MAIN_MENU


async def main() -> None:
    persistence = PicklePersistence(filepath="bridge_bot")
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    await application.bot.set_webhook(
        url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES
    )

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
                CallbackQueryHandler(magaz, pattern="^market$"),
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
            APPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, apps),
                MessageHandler(filters.Document.ALL, apps),
                MessageHandler(filters.PHOTO, apps),
            ],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
            FINISH: [
                CallbackQueryHandler(start, pattern="^main_menu$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish),
            ],
            NAME_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, name_market)
            ],
            NUMBER_MOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, number_mounter)
            ],
            COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, comment_mounter),
                
            ],
            FINISH_AMOUNTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish_amounter),
                CallbackQueryHandler(start, pattern="^main_menu_mounter$"),
            ],
            BRIDG_MARKET: [
                CallbackQueryHandler(start, pattern="^exit$"),
                CallbackQueryHandler(agreed_market, pattern="^buyer$"),
                CallbackQueryHandler(magaz),
            ],
            AGREED_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, agreed_market),
                CallbackQueryHandler(delivery, pattern="^agreed_market$"),
                CallbackQueryHandler(start, pattern="^no_agreed_market$"),
            ],
            BUSINESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, business),
                CallbackQueryHandler(agree_business, pattern="^start_business$"),
                CallbackQueryHandler(start, pattern="^back_to_main_menu$"),
            ],
            AGREED_BUSINES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, agreed_gas),
                CallbackQueryHandler(name_business, pattern="^agreed_business$"),
                CallbackQueryHandler(start, pattern="^no_agreed_business$"),
            ],
            PHONE_BUSINESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone_business)
            ],
            FINISH_BUSINES: [
                CallbackQueryHandler(start, pattern="^finish_business$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish_business),
            ],
            NUMBER_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, number_market)
            ],
            COMMENT_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, comment_market),
                
            ],
            FINISH_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish_market),
                CallbackQueryHandler(start, pattern="^main_menu_market$"),
            ],

        },
        name="bridge_bot",
        persistent=True,
        fallbacks=[CommandHandler("start", start), MessageHandler(filters.Document.ALL, apps)],
    )

    application.add_handler(conv_handler)

    # Set up webserver
    fastapi_app = FastAPI()

    @fastapi_app.post("/telegram")
    async def telegram(req: Request) -> Response:
        data = await req.json()
        await application.update_queue.put(
            Update.de_json(data=data, bot=application.bot)
        )
        return Response(status_code=status.HTTP_200_OK)

    @fastapi_app.get("/healthcheck")
    async def health() -> Response:
        return Response(
            "Я жив", status_code=status.HTTP_200_OK, media_type="text/plain"
        )

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=fastapi_app, port=PORT, host="0.0.0.0", log_level="info"
        )
    )

    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
