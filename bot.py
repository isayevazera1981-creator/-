import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Для мгновенного вывода логов в консоль
sys.stdout.reconfigure(line_buffering=True)

TOKEN = os.environ.get("BOT_TOKEN", "9128067113:AAGwO4mQvg-NNjXrGs2xyklZur0h8ZdmvJI")

bot = telebot.TeleBot(TOKEN)

INFO_TEXT = (
    "✨ *Что умеет бот:*\n\n"
    "🔹 *объясняет темы по русскому языку* (орфография, пунктуация, лексика, морфология, синтаксис, стилистика) простым и понятным языком;\n"
    "🔹 *разбирает произведения и темы по литературе*: сюжет, герои, проблематика, средства выразительности;\n"
    "🔹 *составляет тренировочные тесты и задания* по выбранной теме и уровню сложности;\n"
    "🔹 *проверяет ваши ответы*, показывает ошибки и объясняет правильное решение;\n"
    "🔹 *помогает писать эссе и сочинения*: структура, аргументы, речевые клише, проверка текста;\n"
    "🔹 *предлагает план подготовки* и напоминает, какие темы стоит повторить."
)

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📖 Русский язык")
    btn2 = types.KeyboardButton("📚 Литература")
    btn3 = types.KeyboardButton("📝 Тесты и задания")
    btn4 = types.KeyboardButton("✍️ Сочинения и эссе")
    btn5 = types.KeyboardButton("📅 План подготовки")
    btn6 = types.KeyboardButton("ℹ️ Что умеет бот")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username
    
    # 1. Приветствие по условию
    if username:
        greeting = f"Здравствуйте {username}"
        print(f"Ответил пользователю @{username}")
    else:
        greeting = "Уважаемый клиент,мы стараемся предоставить всю необходимую информацию по подготовке к экзамену по русскому языку и литературе"
        print("Ответил пользователю без username")
    
    bot.reply_to(message, greeting)
    
    # 2. Меню с пояснениями возможностей
    bot.send_message(
        message.chat.id, 
        INFO_TEXT, 
        parse_mode="Markdown", 
        reply_markup=get_main_menu()
    )

# Обработчики кнопок меню
@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Что умеет бот")
def handle_info(message):
    bot.send_message(message.chat.id, INFO_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📖 Русский язык")
def handle_russian(message):
    text = (
        "📖 *Русский язык:*\n\n"
        "Выберите интересующий раздел:\n"
        "1. Орфография (правила написания слов)\n"
        "2. Пунктуация (знаки препинания)\n"
        "3. Морфология и части речи\n"
        "4. Синтаксис (предложения и словосочетания)\n"
        "5. Стилистика и культура речи\n\n"
        "💡 _Напишите интересующую тему или вопрос, и я подробно всё объясню!_"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📚 Литература")
def handle_literature(message):
    text = (
        "📚 *Литература:*\n\n"
        "Здесь мы разбираем:\n"
        "• Сюжет и композицию произведений\n"
        "• Образы и характеры главных героев\n"
        "• Проблематику и авторскую позицию\n"
        "• Средства художественной выразительности (метафоры, эпитеты и др.)\n\n"
        "💡 _Напишите название произведения или автора, который вас интересует._"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📝 Тесты и задания")
def handle_tests(message):
    text = (
        "📝 *Тренировочные тесты:*\n\n"
        "Готовы проверить свои знания?\n"
        "Вы можете решать практические задания с мгновенной проверкой ошибок и разбором правильных ответов."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "✍️ Сочинения и эссе")
def handle_essays(message):
    text = (
        "✍️ *Сочинения и эссе:*\n\n"
        "Помощь в подготовке к письменным работам:\n"
        "• Правильная структура и композиция\n"
        "• Подбор литературных аргументов\n"
        "• Речевые клише и связки\n"
        "• Разбор типичных ошибок"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📅 План подготовки")
def handle_plan(message):
    text = (
        "📅 *План подготовки:*\n\n"
        "Системный подход — залог высокого балла на экзамене!\n"
        "Мы распределим темы, настроим регулярные повторения и тестирование сложных тем."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Мини веб-сервер для бесплатного тарифа Render (Web Service)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Telegram Bot is running!")

    def log_message(self, format, *args):
        pass  # Отключаем лишний спам в логах веб-сервера

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

if __name__ == '__main__':
    # Запускаем фоновый веб-сервер для Render
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    print("Бот успешно запущен и ожидает сообщений...")
    bot.infinity_polling()
