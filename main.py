from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from functional_module import choose_program

# Данные callback
start_data, GENDER_CHOICE_FEMALE, GENDER_CHOICE_MALE, AGE_CHOICE_25, AGE_CHOICE_45, \
    AIM_CHOICE_GAIN, AIM_CHOICE_LOSE, DAYS_CHOICE_2, DAYS_CHOICE_3, DAYS_CHOICE_4 = range(10)

# Данные для подбора тренировок
personal_data = [None, None, None, None]


def start(update, _):
    """Вызывается по команде `/start`."""
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Начнем же!", callback_data=str(start_data)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправление сообщения с клавиатурой
    update.message.reply_text(
        text="Привет! Я бот, созданный для помощи в подборе программы тренировок!", reply_markup=reply_markup
    )
    return


def select_gender(update, _):
    """Ответ на повторный /start"""
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Я - мужчина", callback_data=str(GENDER_CHOICE_MALE)),
            InlineKeyboardButton("Я - женщина", callback_data=str(GENDER_CHOICE_FEMALE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправление сообщения с клавиатурой
    query.edit_message_text(
        text="Для начала выбери свой пол.",
        reply_markup=reply_markup
    )
    return


def select_age(update, _):
    """Выбор возраста"""
    query = update.callback_query
    action = query.data
    if action == '2':
        # Если мужской пол
        personal_data[0] = 'male'
    else:
        # Если женский пол
        personal_data[0] = 'female'
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Мне от 18 до 25", callback_data=str(AGE_CHOICE_25)),
            InlineKeyboardButton("Мне от 25 до 45", callback_data=str(AGE_CHOICE_45)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выбери свой возраст", reply_markup=reply_markup
    )
    return


def select_aim(update, _):
    """Выбор цели тренировок"""
    query = update.callback_query
    query.answer()
    action = query.data
    if action == '3':
        # Если возраст до 25
        personal_data[1] = '25'
    else:
        # Если возраст до 45
        personal_data[1] = '45'
    keyboard = [
        [
            InlineKeyboardButton("Похудеть", callback_data=str(AIM_CHOICE_LOSE)),
            InlineKeyboardButton("Набрать массу", callback_data=str(AIM_CHOICE_GAIN)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Какова цель занятий?", reply_markup=reply_markup
    )
    return


def select_days(update, _):
    """Выбор периодичности занятий"""
    query = update.callback_query
    query.answer()
    action = query.data
    if action == '6':
        # Если цель - похудеть
        personal_data[2] = 'lose'
    else:
        # Если цель - набрать массу
        personal_data[2] = 'gain'
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(DAYS_CHOICE_2)),
            InlineKeyboardButton("3", callback_data=str(DAYS_CHOICE_3)),
            InlineKeyboardButton("4", callback_data=str(DAYS_CHOICE_4)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Сколько раз в неделю хотите заниматься??", reply_markup=reply_markup
    )
    # Переход в состояние разговора `SECOND`
    return


def end(update, _):
    """Окончание диалога"""
    query = update.callback_query
    action = query.data
    if action == '7':
        # Если тренировки 3 дня в неделю
        personal_data[3] = '2'
    elif action == '8':
        # Если тренировки 3 дня в неделю
        personal_data[3] = '3'
    else:
        # Если тренировки 4 дня в неделю
        personal_data[3] = '4'

    query.edit_message_text(text=choose_program(personal_data))
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater("5077017228:AAEoPucavYqlAElV3NA7uOLtkCsVwsppe4A")
    dispatcher = updater.dispatcher

    # Обработчик диалога
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CallbackQueryHandler(select_gender, pattern=str(start_data)))

    dispatcher.add_handler(CallbackQueryHandler(select_age, pattern=str(GENDER_CHOICE_FEMALE)))
    dispatcher.add_handler(CallbackQueryHandler(select_age, pattern=str(GENDER_CHOICE_MALE)))

    dispatcher.add_handler(CallbackQueryHandler(select_aim, pattern=str(AGE_CHOICE_25)))
    dispatcher.add_handler(CallbackQueryHandler(select_aim, pattern=str(AGE_CHOICE_45)))

    dispatcher.add_handler(CallbackQueryHandler(select_days, pattern=str(AIM_CHOICE_GAIN)))
    dispatcher.add_handler(CallbackQueryHandler(select_days, pattern=str(AIM_CHOICE_LOSE)))

    dispatcher.add_handler(CallbackQueryHandler(end, pattern=str(DAYS_CHOICE_2)))
    dispatcher.add_handler(CallbackQueryHandler(end, pattern=str(DAYS_CHOICE_3)))
    dispatcher.add_handler(CallbackQueryHandler(end, pattern=str(DAYS_CHOICE_4)))

    updater.start_polling()
    updater.idle()
