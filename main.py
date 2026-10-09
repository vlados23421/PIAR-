import os
import threading
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
from flask import Flask

# ================= НАСТРОЙКИ =================
# Токен берем из переменных окружения (безопасно для Render)
TOKEN = os.environ.get("VK_TOKEN", "ТВОЙ_НОВЫЙ_ТОКЕН_ЗДЕСЬ")

# ID беседы (чата), куда бот будет отправлять приветствие (если нужно)
# Можно узнать через getConversations или в ссылке чата (последние цифры)
CHAT_ID = 1  # Замените на ID вашего чата, если нужно

# Инициализация бота
bot = Bot(token=TOKEN)

# ================= КЛАВИАТУРЫ =================
def get_main_keyboard():
    """Главное меню с кнопками"""
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("📋 Прайс-лист"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("🔗 Ссылка на чат"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("📜 Правила"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("🆘 Помощь"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

# ================= ОБРАБОТЧИКИ КОМАНД =================

@bot.on.message(text=["Начать", "start", "привет", "меню"])
async def start_handler(message: Message):
    """Приветствие и главное меню"""
    await message.answer(
        "👋 Добро пожаловать в ПИАР ЧАТ | SAMP | CRMP!\n\n"
        "Я — информационный бот. Помогу найти нужную информацию.\n\n"
        "Выберите действие на клавиатуре ниже 👇",
        keyboard=get_main_keyboard()
    )

@bot.on.message(text=["📋 Прайс-лист", "прайс", "цены", "прайс-лист"])
async def price_handler(message: Message):
    """Выдача прайс-листа"""
    await message.answer(
        "💰 ПРАЙС-ЛИСТ\n\n"
        "🎁 БОНУС:\n"
        "Пригласи 30 участников — получи роль «Модератор» бесплатно!\n\n"
        "📌 ПЛАТНОЕ ЗАКРЕПЛЕНИЕ СООБЩЕНИЙ:\n"
        "• 10 минут — 20 ₽\n"
        "• 30 минут — 40 ₽\n"
        "• 50 минут — 60 ₽\n"
        "• 120 минут — 120 ₽\n\n"
        "💳 Оплата — администратору чата.\n"
        "📩 Вопросы — в ЛС сообщества.",
        keyboard=get_main_keyboard()
    )

@bot.on.message(text=["🔗 Ссылка на чат", "ссылка", "чат", "вступить"])
async def link_handler(message: Message):
    """Выдача ссылки на чат"""
    await message.answer(
        "🔗 ССЫЛКА НА ПИАР ЧАТ:\n\n"
        "https://vk.me/join/kuBhzS34RI7dc8140qevGBk11iBjwb8mcGk=\n\n"
        "Переходи и пропиарь свой сервер!",
        keyboard=get_main_keyboard()
    )

@bot.on.message(text=["📜 Правила", "правила", "rules"])
async def rules_handler(message: Message):
    """Выдача правил чата"""
    await message.answer(
        "📜 ПРАВИЛА ЧАТА:\n\n"
        "1. Уважай других участников.\n"
        "2. Запрещён спам и флуд.\n"
        "3. Пиар только по теме SAMP/CRMP.\n"
        "4. Не оскорбляй администрацию.\n"
        "5. Соблюдай правила ВКонтакте.\n\n"
        "За нарушение — бан без предупреждения.",
        keyboard=get_main_keyboard()
    )

@bot.on.message(text=["🆘 Помощь", "помощь", "help"])
async def help_handler(message: Message):
    """Помощь по командам"""
    await message.answer(
        "🆘 ПОМОЩЬ\n\n"
        "Доступные команды:\n"
        "• Начать / Меню — показать главное меню\n"
        "• Прайс — узнать цены\n"
        "• Ссылка — получить ссылку на чат\n"
        "• Правила — прочитать правила\n\n"
        "📩 Если что-то не работает — пиши в ЛС сообщества.",
        keyboard=get_main_keyboard()
    )

# ================= FLASK ДЛЯ RENDER =================
app = Flask(__name__)

@app.route("/health")
def health():
    """Эндпоинт для Better Stack, чтобы бот не засыпал"""
    return "Bot is alive", 200

def run_flask():
    """Запуск Flask в отдельном потоке"""
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ================= ЗАПУСК =================
if __name__ == "__main__":
    # Запускаем Flask в фоне (для Render)
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запускаем бота
    print("Бот запущен и слушает сообщения...")
    bot.run_forever()
