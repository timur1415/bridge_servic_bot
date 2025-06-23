from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import BRIDG_MARKET, AGREED_MARKET, NAME_MOUNTER

from config.tovari import GOODS_INFO


async def magaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⬅️", callback_data="left"),
            InlineKeyboardButton("➡️", callback_data="right"),
        ],
        [InlineKeyboardButton("выход", callback_data="exit")],
        [InlineKeyboardButton("Оставить заявку", callback_data="buyer")],
    ]

    if query.data == "magaz":
        context.user_data["n_page"] = 1
    elif query.data == "left":
        context.user_data["n_page"] -= 1
    elif query.data == "right":
        context.user_data["n_page"] += 1

    if context.user_data.get("n_page"):
        n_page = context.user_data.get("n_page")
    else:
        context.user_data["n_page"] = 1
        n_page = context.user_data.get("n_page")

    if n_page > 3:
        context.user_data["n_page"] = 3
    if n_page < 1:
        context.user_data["n_page"] = 1

    with open(GOODS_INFO[n_page]["photo"], "rb") as photo:
        await query.edit_message_media(media=InputMediaPhoto(media=photo))

        await query.edit_message_caption(
            caption=f"{GOODS_INFO[n_page]['text']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    return BRIDG_MARKET

async def agreed_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("✅согласен✅", callback_data="agreed_market"),
            InlineKeyboardButton("❌не согласен❌", callback_data="no_agreed_market"),
        ],
        [
            InlineKeyboardButton(
                "согласие на передачу и обработку персональных данных",
                url="https://bridge-service.ru/user/agreement/",
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",reply_markup=markup
    )
    return AGREED_MARKET

async def delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [["до квартиры"], ["до подъезда"], ["самовывоз"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите вариант доставки",
        reply_markup=markup
    )
    return NAME_MOUNTER