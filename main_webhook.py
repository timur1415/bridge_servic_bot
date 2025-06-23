
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
    NAME_MOUNTER
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
    agreed_gas
)

from handlers.mounter import fitter, agreeds_mounter, name_mounter, number_mounter, comment_mounter, finish_amounter

from handlers.shop_handler import shop

from handlers.business_handler import business

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


async def main() -> None:
    persistence = PicklePersistence(filepath="bridge_bot")
    application = (
        Application.builder().token(TOKEN).persistence(persistence).build()
    )

    await application.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)

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
            APPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, apps)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
            FINISH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, finish),
                CallbackQueryHandler(start, pattern="^main_menu$"),
            ],
            NAME_MOUNTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_mounter)],
            NUMBER_MOUNTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number_mounter)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comment_mounter),
                      CallbackQueryHandler(start, pattern='^main_menu_mounter$')],
            FINISH_AMOUNTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_amounter)],
            BRIDG_MARKET: [CallbackQueryHandler(start, pattern="^exit$"),
                           CallbackQueryHandler(agreed_market, pattern='^buyer$'),
                CallbackQueryHandler(magaz)],
            AGREED_MARKET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, agreed_market),
                CallbackQueryHandler(delivery, pattern="^agreed_market$"),
                CallbackQueryHandler(start, pattern="^no_agreed_market$"),
            ],
        },
        name="bridge_bot",
        persistent=True,
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # Set up webserver
    fastapi_app = FastAPI()

    @fastapi_app.post("/telegram")  
    async def telegram(req: Request) -> Response:
        data = await req.json()
        await application.update_queue.put(Update.de_json(data=data, bot=application.bot))
        return Response(status_code=status.HTTP_200_OK)


    @fastapi_app.get("/healthcheck")
    async def health() -> Response:
        return Response('я жив', status_code=status.HTTP_200_OK, media_type='text/plain')

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=fastapi_app,
            port=PORT,
            host="0.0.0.0",
            log_level = 'info' 
        )
    )


    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())