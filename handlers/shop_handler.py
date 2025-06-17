import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)

from config.states import SHOP, FITTER, AGREED


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def fitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Оставить заявку", callback_data="leave")],
        [
            InlineKeyboardButton("Наш магазин", url="https://bridgemag.ru/"),
            InlineKeyboardButton("WhatsApp", url="https://wa.me/79175882277"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/main_shop.jpg", "rb"),
        caption="Газовое оборудование и расходники для монтажников – оптом и в розницу!\n\nПредоставляем объекты на подряд для профессионалов!\n\nВсё для профессионального монтажа.\n\nИщете надежного поставщика газового оборудования и комплектующих для монтажа? Мы предлагаем широкий ассортимент продукции по выгодным ценам!\n\nНаши специалисты помогут вам подобрать необходимое оборудование и комплектующие для вашего проекта.",
        reply_markup=markup,
    )
    return FITTER


async def agreeds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("✅согласен✅", callback_data="agreed"),
            InlineKeyboardButton("❌не согласен❌", callback_data="no_agreed"),
        ],
        [
            InlineKeyboardButton(
                "согласие на передачу и обработку персональных данных",
                url="https://bridge-service.ru/user/agreement/",
            )
        ],
        [
            InlineKeyboardButton(
                "политику конфиденциальности",
                url="https://bridge-service.ru/politika-konfidencialnosti/",
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",
        reply_markup=markup,
    )
    return AGREED
