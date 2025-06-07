from telebot import types
import telebot
from db import get_categories, get_questions_by_category, get_answer


# Инициализация бота с токеном
bot = telebot.TeleBot('7889683160:AAElwBpEruLYgDecXDfxpVFU6DYD_csl-Q8')
user_states = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    categories = get_categories()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        keyboard.add(types.KeyboardButton(category))
    bot.send_message(message.chat.id, 'Привет! 👋 Я твой помощник в проектном обучении. Выбери вопрос который тебя интересует, а я с удовольствием на него отвечу 😊', reply_markup=keyboard)
    user_states[message.chat.id] = None  # сброс выбора

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    state = user_states.get(chat_id)
    categories = get_categories()

    if text in categories:
        # Пользователь выбрал категорию, показываем вопросы этой категории
        user_states[chat_id] = text
        questions = get_questions_by_category(text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for question in questions:
            keyboard.add(types.KeyboardButton(question))
        keyboard.add(types.KeyboardButton('🔙 Назад'))
        bot.send_message(chat_id, f'Вы выбрали раздел "{text}". Теперь выберите вопрос:', reply_markup=keyboard)
    elif text == '🔙 Назад':
        # Возврат к категориям
        user_states[chat_id] = None
        categories = get_categories()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            keyboard.add(types.KeyboardButton(category))
        bot.send_message(chat_id, 'Выберите раздел:', reply_markup=keyboard)
    elif state:
        # Выбрана категория, значит выбирают вопрос
        answer = get_answer(text)
        bot.send_message(chat_id, answer)
    else:
        # Если что-то не совпало — возвращаем к началу
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            keyboard.add(types.KeyboardButton(category))
        bot.send_message(chat_id, 'Выберите раздел:', reply_markup=keyboard)
        user_states[chat_id] = None

# Запуск бота
bot.polling(none_stop=True)