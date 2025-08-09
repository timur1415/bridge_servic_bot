from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    BRIDG_MARKET,
    AGREED_MARKET,
    NAME_MARKET,
    COMMENT_MARKET,
    FINISH_MARKET,
    NUMBER_MARKET,
)

from config.tovari import GOODS_INFO

from servises.crm_lead_add import send_market_lead


async def magaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("⬅️", callback_data="left"),
            InlineKeyboardButton("➡️", callback_data="right"),
        ],
        [InlineKeyboardButton("Выход", callback_data="exit")],
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
            InlineKeyboardButton("✅Согласен✅", callback_data="agreed_market"),
            InlineKeyboardButton("❌Не согласен❌", callback_data="no_agreed_market"),
        ],
        [
            InlineKeyboardButton(
                "Согласие на передачу и обработку персональных данных",
                url="https://bridge-service.ru/user/agreement/",
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",
        reply_markup=markup,
    )
    return AGREED_MARKET


async def delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [["До квартиры"], ["До подъезда"], ["Самовывоз"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите вариант доставки",
        reply_markup=markup,
    )
    return NAME_MARKET


async def name_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["delivery"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Как вас зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NUMBER_MARKET


async def number_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, оставьте номер телефона",
    )
    return COMMENT_MARKET


async def comment_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Оставьте комментарий, что именно вы хотите приобрести",
    )
    return FINISH_MARKET


async def finish_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comment"] = update.effective_message.text
    keyboard = [
        [InlineKeyboardButton("В главное меню", callback_data="main_menu_market")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо за обращение! Мы свяжемся с Вами в ближайшее время",
        reply_markup=markup,
    )
    await send_market_lead(
        context.user_data["delivery"],
        context.user_data["name"],
        context.user_data["number"],
        context.user_data["comment"],
    )
