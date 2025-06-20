from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
)

from config.states import (
    AGREED,
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


async def agreed(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",reply_markup=markup
    )
    return AGREED


async def gas_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "РАССЧИТАТЬ СТОИМОСТЬ ГАЗИФИКАЦИИ", callback_data="start_gas"
            )
        ],
        [InlineKeyboardButton("в главное меню", callback_data="back")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/gas.jpg", "rb"),
        caption="Газификация и инженерные системы любой сложности.\n\nГазификация под ключ от профессионалов: надежные решения для вашего комфорта.\n\nМы предлагаем полный спектр услуг, начиная с консультирования и проектирования, продолжая монтажными и пуско-наладочными работами и завершая гарантийным и постгарантийным обслуживанием оборудования. \n\nДоверьте свой комфорт профессионалам.\n\nПри нажатии кнопки «Рассчитать стоимость газификации» вы подтверждаете согласие на обработку и передачу персональных данных.",
        reply_markup=markup,
    )
    return GAS_START


async def terrain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Где вы находитесь территориально?",
    )
    return WHEN


async def when(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["в течении месяца"], ["в течении полугода"], ["в течении года"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Когда планируете начать процесс газификации?",
        reply_markup=markup,
    )
    return PROJECT


async def project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["да"], ["нет"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Есть ли проект?",
        reply_markup=markup,
    )
    return ROOM


async def room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["в одном"], ["в рразных"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Газоиспользующее оборудование находится в одном помещении или в разных?",
        reply_markup=markup,
    )
    return METRE


async def metre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["0-5"], ["5-10"], ["10-15"], ["15-25"], ["более 25"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сколько метров от забора до угла дома?",
        reply_markup=markup,
    )
    return FACADE


async def fasade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["0-5"], ["5-10"], ["10-15"], ["15-25"], ["более 25"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сколько метров по фасаду дома до дальней точки газа использующегося оборудования?",
        reply_markup=markup,
    )
    return PRESSURE


async def pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["среднее", "низкое"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Какое давление газа в распределительном газопроводе?",
        reply_markup=markup,
    )
    return DOCUMENTS


async def documents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Загрузите документы для заявления на газификацию:\n\nНеобходимые документы для газификации:\n\n1. Паспорт собственника: основная страница и прописка;\n2. Выписка ЕГРН на дом (все листы);\n3. Выписка ЕГРН на землю (все листы);\n4. Поэтажный план дома;\n5. СНИЛС;\n6. ИНН;\n7. Доверенность.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return APPS


async def apps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["watsApp"], ["звонок"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="как вам удобней получить расчёт?",
        reply_markup=markup,
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напишите ваше имя.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NUMBER


async def number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Напишите ваш контактный номер телефона:"
    )
    return FINISH


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("вернутся в главное меню", callback_data="main_menu")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо за обращение! Мы свяжемся с Вами в ближайшее время",
        reply_markup=markup,
    )
