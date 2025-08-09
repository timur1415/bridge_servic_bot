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
from config.states import (
    SHOP,
    MOUNTER,
    AGREED_MOUNTER,
    NUMBER_MOUNTER,
    COMMENT,
    FINISH_AMOUNTER,
)

from servises.crm_lead_add import send_mounter_lead


async def fitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    query = update.callback_query
    query.answer()
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
        photo=open("photo/m_1.jpg", "rb"),
        caption="Газовое оборудование и расходники для монтажников – оптом и в розницу!\n\nПредоставляем объекты на подряд для профессионалов!\n\nВсё для профессионального монтажа.\n\nИщете надежного поставщика газового оборудования и комплектующих для монтажа? Мы предлагаем широкий ассортимент продукции по выгодным ценам!\n\nНаши специалисты помогут вам подобрать необходимое оборудование и комплектующие для вашего проекта.",
        reply_markup=markup,
    )
    return MOUNTER


async def agreeds_mounter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("✅согласен✅", callback_data="agreed_mounter"),
            InlineKeyboardButton("❌не согласен❌", callback_data="no_agreed_mounter"),
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
        # TODO pomenyt text
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",
        reply_markup=markup,
    )
    return AGREED_MOUNTER


async def name_mounter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Как вас зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NUMBER_MOUNTER


async def number_mounter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name_mounter"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста оставьте свой номер номер телефона",
    )
    return COMMENT


async def comment_mounter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number_mounter"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Оставьте комментарий, что именно вы хотите приобрести",
    )
    return FINISH_AMOUNTER


async def finish_amounter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comment_mounter"] = update.effective_message.text
    keyboard = [
        [InlineKeyboardButton("в главное меню", callback_data="main_menu_mounter")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо за обращение! Мы свяжемся с Вами в ближайшее время",
        reply_markup=markup,
    )
    await send_mounter_lead(
        context.user_data["name_mounter"],
        context.user_data["comment_mounter"],
        context.user_data["number_mounter"],
    )
