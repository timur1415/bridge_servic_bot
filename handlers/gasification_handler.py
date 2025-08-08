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
    AGREED_GAS,
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

from crm_lead_add import send_gasification_lead


async def agreed_gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("✅согласен✅", callback_data="agreed"),
            InlineKeyboardButton("❌не согласен❌", callback_data="no_agreed"),
        ],
        [
            InlineKeyboardButton(
                "Согласие на передачу и обработку персональных данных",
                url="https://bridge-service.ru/user/agreement/",
            )
        ],
        [
            InlineKeyboardButton(
                "Политика конфиденциальности",
                url="https://bridge-service.ru/politika-konfidencialnosti/",
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Для определения стоимости услуг газификации необходимо ваше согласие на обработку и передачу персональных данных.",reply_markup=markup
    )
    return AGREED_GAS


async def gas_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()    
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
    context.user_data['terrain'] = update.effective_message.text

    keyboard = [["в течении месяца"], ["в течении полугода"], ["в течении года"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Когда планируете начать процесс газификации?",
        reply_markup=markup,
    )
    return PROJECT


async def project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['when'] = update.effective_message.text

    keyboard = [["Да"], ["нет"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Есть ли проект?",
        reply_markup=markup,
    )
    return ROOM


async def room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['project'] = update.effective_message.text
    keyboard = [["в одном"], ["в разных"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Газоиспользующее оборудование находится в одном помещении или в разных?",
        reply_markup=markup,
    )
    return METRE


async def metre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['room'] = update.effective_message.text
    keyboard = [["0-5"], ["5-10"], ["10-15"], ["15-25"], ["более 25"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сколько метров от забора до угла дома?",
        reply_markup=markup,
    )
    return FACADE


async def fasade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['metre'] = update.effective_message.text
    keyboard = [["0-5"], ["5-10"], ["10-15"], ["15-25"], ["более 25"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сколько метров по фасаду дома до дальней точки газа использующегося оборудования?",
        reply_markup=markup,
    )
    return PRESSURE


async def pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fasade'] = update.effective_message.text
    keyboard = [["среднее", "низкое"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Какое давление газа в распределительном газопроводе?",
        reply_markup=markup,
    )
    return DOCUMENTS


async def documents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['pressure'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Загрузите документы для заявления на газификацию:\n\nНеобходимые документы для газификации:\n\n1. Паспорт собственника: основная страница и прописка;\n2. Выписка ЕГРН на дом (все листы);\n3. Выписка ЕГРН на землю (все листы);\n4. Поэтажный план дома;\n5. СНИЛС;\n6. ИНН;\n7. Доверенность.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return APPS


async def apps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.effective_message.document
    print(document)
    
    file = await document.get_file()
    file_path = await file.download_to_drive()
    print(file_path)


    keyboard = [["WhatsApp"], ["звонок"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="как вам удобней получить расчёт?",
        reply_markup=markup,
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['apps'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напишите ваше имя.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NUMBER


async def number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Напишите ваш контактный номер телефона:"
    )
    return FINISH


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['number'] = update.effective_message.text
    keyboard = [
        [InlineKeyboardButton("вернутся в главное меню", callback_data="main_menu")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо за обращение! Мы свяжемся с Вами в ближайшее время",
        reply_markup=markup,
    )
    gas_dict = {'name': context.user_data['name'], 'apps': context.user_data['apps'], 'pressure': context.user_data['pressure'], 'fasade': context.user_data['fasade'], 'metre': context.user_data['metre'], 'room': context.user_data['room'], 'project': context.user_data['project'], 'when': context.user_data['when'], 'terrain': context.user_data['terrain'], 'number': context.user_data['number']}
    
    await send_gasification_lead(gas_dict)
