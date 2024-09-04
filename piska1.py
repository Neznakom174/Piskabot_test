import telebot
from random import randint
from datetime import datetime, timedelta
from telebot import types
import json
import os

# Токен вашего бота
TOKEN = '7223596415:AAEGrp6DZbSogoFSyjtlNNujWkphWOKLcEE'
bot = telebot.TeleBot(TOKEN)

# Файл для сохранения данных пользователей
DATA_FILE = 'user_data.json'

# Словарь для хранения данных пользователей
user_data = {}

# Функция загрузки данных из файла
def load_data():
    global user_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            user_data = json.load(file)

# Функция сохранения данных в файл
def save_data():
    with open(DATA_FILE, 'w') as file:
        json.dump(user_data, file)

# Функция создания клавиатуры команд
def create_command_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    dick_button = types.KeyboardButton(text="/dick")
    size_button = types.KeyboardButton(text="/size")
    keyboard.add(dick_button, size_button)
    return keyboard

# Функция обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = create_command_keyboard()
    bot.send_message(message.chat.id, "Привет! Используйте команду /dick, чтобы 'вырастить пипису'. Команду можно использовать только раз в день. Вы также можете использовать команду /size, чтобы узнать текущий размер.", reply_markup=keyboard)

# Функция обработки команды /dick
@bot.message_handler(commands=['dick'])
def dick(message):
    user_id = str(message.from_user.id)

    # Инициализация данных пользователя, если их нет
    if user_id not in user_data:
        user_data[user_id] = {'size': 0, 'last_used': None}

    user_info = user_data[user_id]

    # Проверка на использование команды раз в день
    now = datetime.now()

    if user_info['last_used'] and now - datetime.fromisoformat(user_info['last_used']) < timedelta(days=1):
        bot.reply_to(message, "Эту команду можно использовать только раз в день.")
        return

    # Обновление времени последнего использования команды
    user_info['last_used'] = now.isoformat()

    # Рандомное увеличение размера от 2 до 10 см
    increase = randint(2, 10)
    user_info['size'] += increase

    # Иногда уменьшаем размер
    if randint(1, 100) <= 10:  # 10% шанс уменьшения
        decrease = randint(2, 5)
        user_info['size'] = max(user_info['size'] - decrease, 0)  # Размер не может быть меньше 0

    # Сохранение данных
    save_data()

    # Отправляем сообщение пользователю
    bot.reply_to(message, f"Вырастили пипису на {increase} см. Текущий размер: {user_info['size']} см.")

# Функция обработки команды /size
@bot.message_handler(commands=['size'])
def size(message):
    user_id = str(message.from_user.id)

    # Проверка, есть ли данные о пользователе
    if user_id not in user_data:
        bot.reply_to(message, "Ваш размер еще не установлен. Используйте команду /dick, чтобы начать рост.")
    else:
        current_size = user_data[user_id]['size']
        bot.reply_to(message, f"Текущий размер вашей пиписки: {current_size} см.")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_unknown_message(message):
    bot.reply_to(message, "Я не понимаю, о чем вы говорите. Попробуйте использовать команду /dick или /size.")

# Загрузка данных при старте бота
load_data()

# Запуск бота
bot.polling(none_stop=True)
