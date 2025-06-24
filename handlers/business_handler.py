import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
from config.states import BUSINESS, AGREED_BUSINES, FINISH_BUSINES, PHONE_BUSINESS


async def business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Оставить заявку", callback_data="start_business")],
        [
            InlineKeyboardButton(
                "Наш сайт",
                url="https://bridge-service.ru/gazifikaciya-kommercheskih-ob-ektov/",
            ),
            InlineKeyboardButton("выход", callback_data="beck_to_main_menu"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open("photo/video.mp4", "rb"),
        caption="Газификация коммерческих объектов.\n\nРаботаем «ПОД КЛЮЧ»\n\nКОМПЛЕКСНЫЕ РЕШЕНИЯ ОТ ЭКСПЕРТОВ С ГАРАНТИЕЙ КАЧЕСТВА\n\nПроекты, позволяющие сократить издержки при эксплуатации.Берем на себя все заботы по оформлению документов, проектированию, монтажу и эксплуатации минимально вовлекая вас в рабочие задачи.\n\nОперативное, точное исполнение и регулярное обслуживание для минимизации рисков.",
        reply_markup=markup,
    )
    return BUSINESS


async def agree_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("✅согласен✅", callback_data="agreed_busines"),
            InlineKeyboardButton("❌не согласен❌", callback_data="no_agreed_busines"),
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
    return AGREED_BUSINES


async def name_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Как вас зовут?"
    )
    return PHONE_BUSINESS

async def phone_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="какой у вас номер телефона"
    )
    return FINISH_BUSINES

async def finish_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton('выход', callback_data='finish_business')]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="спасибо за обращение в ближайшее время мы с вами свяжемся", reply_markup=markup
    )
