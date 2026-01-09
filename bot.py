import telebot
from telebot import types
import time
import traceback
import os
import sys
from keep_alive import keep_alive

keep_alive()

# Токен берется из переменных окружения (НОВЫЙ ТОКЕН)
token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(token)

# 🔴 ВАШ TELEGRAM ID
ADMIN_ID = 334976250

# Список магазинов
stores = {
    "005": {
        "name": "Химки",
        "specialist": "Сиваков Кирилл",
        "spec_phone": "+7 (969) 023-80-97"
    },
    "028": {
        "name": "Ногинск",
        "specialist": "Филиппова Евгения",
        "spec_phone": "+7 (963) 772-51-14"
    },
    "143": {
        "name": "Варшавское шоссе",
        "specialist": "Махонин Дмитрий", 
        "spec_phone": "+7 (926) 663-67-93"
    }
    # Добавьте остальные магазины здесь по тому же шаблону
}

# 🔴 УСТАНОВКА КОМАНД МЕНЮ БОТА
def set_bot_commands():
    """Устанавливает команды меню бота"""
    commands = [
        types.BotCommand("start", "Главное меню"),
        types.BotCommand("myid", "Узнать свой ID"),
        types.BotCommand("all", "Все магазины"),
        types.BotCommand("help", "Справка"),
    ]
    
    try:
        bot.set_my_commands(commands)
        print("✅ Команды меню установлены")
    except Exception as e:
        print(f"⚠️ Ошибка установки команд: {e}")

# 🔴 УЛУЧШЕННАЯ ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ
def safe_send_message(chat_id, text, reply_markup=None, parse_mode=None, max_retries=3):
    """Безопасная отправка сообщений с повторными попытками"""
    for attempt in range(max_retries):
        try:
            if reply_markup:
                return bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
            else:
                return bot.send_message(chat_id, text, parse_mode=parse_mode)
        except Exception as e:
            print(f"⚠️ Ошибка отправки сообщения (попытка {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Ждем перед повторной попыткой
            else:
                print(f"❌ Не удалось отправить сообщение после {max_retries} попыток")
                raise

# 🔴 ОБНОВЛЕННОЕ ГЛАВНОЕ МЕНЮ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        if user_id == ADMIN_ID:
            # 🔴 МЕНЮ АДМИНА
            btn1 = types.KeyboardButton("🏪 Показать магазины")
            btn2 = types.KeyboardButton("👑 Админ-панель")
            btn3 = types.KeyboardButton("ℹ️ О боте")
            btn4 = types.KeyboardButton("📝 Обратная связь")
            
            markup.add(btn1, btn2)
            markup.add(btn3, btn4)
            
            welcome_text = (
                f"👑 *Привет, администратор!*\n\n"
                f"В базе: *{len(stores)} магазинов*\n\n"
                f"*Выберите действие:*"
            )
        else:
            # 🔴 МЕНЮ ПОЛЬЗОВАТЕЛЯ
            btn1 = types.KeyboardButton("🏪 Показать магазины")
            btn2 = types.KeyboardButton("ℹ️ О боте")
            btn3 = types.KeyboardButton("📝 Обратная связь")
            
            markup.add(btn1, btn2, btn3)
            
            welcome_text = (
                "👋 *Добро пожаловать в бот 9 региона!*\n\n"
                f"В базе: *{len(stores)} магазинов*\n\n"
                "*Выберите действие:*"
            )
        
        safe_send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в send_welcome: {e}")

# 🔴 О БОТЕ
@bot.message_handler(func=lambda m: m.text == "ℹ️ О боте")
def about_bot(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в меню"))
        
        info_text = (
            "🤖 *Бот 9 региона*\n\n"
            "*Назначение:*\n"
            "Быстрый доступ к контактам ответственных специалистов\n\n"
            "*Функции:*\n"
            "• 🏪 Поиск магазина по номеру\n"
            "• 👤 Контакты ответственного специалиста\n"
            "• 📞 Прямая связь с ответственным\n\n"
            "💡 *Бот постоянно развивается!*\n"
            "Хотите новую функцию? Оставьте обратную связь!\n\n"
            f"*Техническая информация:*\n"
            f"• Магазинов в базе: {len(stores)}\n"
            "• Версия: 1.2\n"
            "• Разработано для 9 региона"
        )
        
        safe_send_message(message.chat.id, info_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в about_bot: {e}")

# 🔴 ОБРАТНАЯ СВЯЗЬ - ИСПРАВЛЕННАЯ ВЕРСИЯ
@bot.message_handler(func=lambda m: m.text == "📝 Обратная связь")
def feedback_menu(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        btn1 = types.KeyboardButton("💡 Предложить улучшение")
        btn2 = types.KeyboardButton("🐛 Сообщить об ошибке")
        btn3 = types.KeyboardButton("◀️ Назад в меню")
        
        markup.add(btn1, btn2, btn3)
        
        response = (
            "📝 *ОБРАТНАЯ СВЯЗЬ*\n\n"
            "💡 *Ваше мнение очень важно для развития бота!*\n\n"
            "Выберите тип обращения:\n\n"
            "• 💡 *Предложить улучшение* — идеи по развитию бота\n"
            "• 🐛 *Сообщить об ошибке* — если что-то работает не так\n\n"
            "*Спасибо, что помогаете делать бот лучше!*"
        )
        
        safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в feedback_menu: {e}")
        bot.reply_to(message, "❌ Ошибка при открытии меню обратной связи")

# 🔴 ОБРАБОТКА ВЫБОРА ТИПА ОБРАТНОЙ СВЯЗИ
@bot.message_handler(func=lambda m: m.text in ["💡 Предложить улучшение", "🐛 Сообщить об ошибке"])
def handle_feedback_type(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❌ Отменить отправку"))
        
        feedback_type = message.text
        
        msg = safe_send_message(
            message.chat.id,
            f"📝 *{feedback_type}*\n\n"
            f"Опишите ваше предложение или ошибку подробно:\n\n"
            f"Или нажмите *❌ Отменить отправку* чтобы вернуться",
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        bot.register_next_step_handler(msg, process_feedback, feedback_type)
    except Exception as e:
        print(f"❌ Ошибка в handle_feedback_type: {e}")

# 🔴 ОБРАБОТКА ТЕКСТА ОБРАТНОЙ СВЯЗИ
def process_feedback(message, feedback_type):
    try:
        # 🔴 ОБРАБОТКА ОТМЕНЫ
        if message.text == "❌ Отменить отправку":
            feedback_menu(message)
            return
        
        user_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        
        # Отправляем сообщение админу
        admin_msg = (
            f"📨 *НОВАЯ ОБРАТНАЯ СВЯЗЬ*\n\n"
            f"*От:* {user_name}\n"
            f"*ID:* `{message.from_user.id}`\n"
            f"*Тип:* {feedback_type}\n\n"
            f"*Сообщение:*\n{message.text}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в меню"))
        
        try:
            bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
            safe_send_message(
                message.chat.id,
                "✅ *Спасибо! Ваше сообщение отправлено администратору.*\n\n"
                "*Мы обязательно рассмотрим ваше предложение!*",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"❌ Ошибка отправки админу: {e}")
            safe_send_message(
                message.chat.id,
                "❌ Ошибка при отправке. Попробуйте позже.",
                reply_markup=markup
            )
        
        print(f"\n📨 ОБРАТНАЯ СВЯЗЬ от {user_name} ({message.from_user.id}): {feedback_type} - {message.text}")
        
    except Exception as e:
        print(f"❌ Ошибка в process_feedback: {e}")

# 🔴 АДМИН-ПАНЕЛЬ (с кнопкой Назад)
@bot.message_handler(func=lambda m: m.text == "👑 Админ-панель")
def admin_panel(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "⛔ Доступ запрещен")
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        btn1 = types.KeyboardButton("📊 Просмотр статистики")
        btn2 = types.KeyboardButton("➕ Добавить магазин")
        btn3 = types.KeyboardButton("✏️ Редактировать магазин")
        btn4 = types.KeyboardButton("📥 Экспорт данных")
        btn5 = types.KeyboardButton("◀️ Назад в меню")
        
        markup.add(btn1, btn2, btn3)
        markup.add(btn4, btn5)
        
        response = (
            "👑 *АДМИН-ПАНЕЛЬ*\n\n"
            "Доступные функции:\n\n"
            "• 📊 Просмотр статистики — информация о боте\n"
            "• ➕ Добавить магазин — новый магазин в базу\n"
            "• ✏️ Редактировать магазин — изменить данные\n"
            "• 📥 Экспорт данных — выгрузить все контакты\n\n"
            "*Используйте кнопки для навигации*"
        )
        
        safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в admin_panel: {e}")

# 🔴 ПРОСТАЯ СТАТИСТИКА
@bot.message_handler(func=lambda m: m.text == "📊 Просмотр статистики")
def show_stats(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "⛔ Доступ запрещен")
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в админ-панель"))
        
        response = (
            "📊 *СТАТИСТИКА БОТА*\n\n"
            f"🏪 Магазинов в базе: {len(stores)}\n"
            f"👷 Специалистов: {len(stores)}\n\n"
            "📈 *Использование:*\n"
            "• Бот запущен и работает\n"
            "• Данные готовы к использованию\n\n"
            "🛠 *Техническая информация:*\n"
            "• Версия бота: 1.2\n"
            "• Python + pyTelegramBotAPI\n"
            f"• Ваш ID: `{ADMIN_ID}`"
        )
        
        safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в show_stats: {e}")

# 🔴 ДОБАВЛЕНИЕ МАГАЗИНА
@bot.message_handler(func=lambda m: m.text == "➕ Добавить магазин")
def add_store_admin(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "⛔ Доступ запрещен")
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❌ Отмена"))
        
        msg = safe_send_message(
            message.chat.id,
            "🏪 *ДОБАВЛЕНИЕ НОВОГО МАГАЗИНА*\n\n"
            "Введите данные в формате:\n"
            "`ID;Название;Специалист;Телефон`\n\n"
            "Пример:\n"
            "`144;Магазин Центральный;Иванов Иван;+7 999 123-45-67`\n\n"
            "Или нажмите *❌ Отмена* чтобы вернуться",
            parse_mode='Markdown',
            reply_markup=markup
        )
        
        bot.register_next_step_handler(msg, process_new_store)
    except Exception as e:
        print(f"❌ Ошибка в add_store_admin: {e}")

def process_new_store(message):
    try:
        if message.from_user.id != ADMIN_ID:
            return
        
        # 🔴 ОБРАБОТКА ОТМЕНЫ
        if message.text == "❌ Отмена":
            admin_panel(message)
            return
        
        parts = message.text.split(';')
        if len(parts) < 4:
            bot.reply_to(message, "❌ Нужно 4 части: ID;Название;Специалист;Телефон")
            return
        
        store_id = parts[0].strip()
        name = parts[1].strip()
        specialist = parts[2].strip()
        phone = parts[3].strip()
        
        if store_id in stores:
            bot.reply_to(message, f"❌ Магазин с ID `{store_id}` уже существует!")
            return
        
        stores[store_id] = {
            "name": name,
            "specialist": specialist,
            "spec_phone": phone
        }
        
        response = (
            f"✅ *Магазин добавлен!*\n\n"
            f"🏪 ID: `{store_id}`\n"
            f"📝 Название: {name}\n"
            f"👤 Специалист: {specialist}\n"
            f"📱 Телефон: {phone}\n\n"
            f"Теперь в базе: {len(stores)} магазинов"
        )
        
        safe_send_message(message.chat.id, response, parse_mode='Markdown')
        admin_panel(message)
        
    except Exception as e:
        print(f"❌ Ошибка в process_new_store: {e}")
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# 🔴 ЭКСПОРТ ДАННЫХ (с кнопкой Назад)
@bot.message_handler(func=lambda m: m.text == "📥 Экспорт данных")
def export_data(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "⛔ Доступ запрещен")
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в админ-панель"))
        
        export_text = "🏪 ЭКСПОРТ ДАННЫХ МАГАЗИНОВ\n\n"
        
        for store_id, store_info in stores.items():
            export_text += f"{store_id};{store_info['name']};{store_info['specialist']};{store_info['spec_phone']}\n"
        
        with open("stores_export.txt", "w", encoding="utf-8") as f:
            f.write(export_text)
        
        with open("stores_export.txt", "rb") as f:
            bot.send_document(message.chat.id, f, caption="📁 Экспорт данных магазинов", reply_markup=markup)
        
        safe_send_message(message.chat.id, "✅ Данные экспортированы в файл!")
    except Exception as e:
        print(f"❌ Ошибка в export_data: {e}")

# 🔴 СПИСОК МАГАЗИНОВ
@bot.message_handler(func=lambda m: m.text == "🏪 Показать магазины")
def show_stores(message):
    try:
        if not stores:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("◀️ Назад в меню"))
            safe_send_message(message.chat.id, "📭 Список магазинов пуст.", reply_markup=markup)
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        for store_id, store_info in stores.items():
            button_text = f"🏪 {store_id} - {store_info['name']}"
            if len(button_text) > 30:
                button_text = button_text[:27] + "..."
            markup.add(types.KeyboardButton(button_text))
        
        markup.add(types.KeyboardButton("◀️ Назад в меню"))
        
        response = (
            "🏪 *Выберите магазин:*\n\n"
            f"*Всего магазинов:* {len(stores)}\n"
            "*Нажмите на нужный магазин или вернитесь в меню*"
        )
        
        safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в show_stores: {e}")

# 🔴 ИНФОРМАЦИЯ О МАГАЗИНЕ
@bot.message_handler(func=lambda m: m.text.startswith("🏪 ") and " - " in m.text)
def show_store_info(message):
    try:
        store_id = message.text.split(" - ")[0].replace("🏪 ", "").strip()
        
        if store_id in stores:
            store = stores[store_id]
            store_name = store['name']
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("◀️ Назад к списку"))
            
            response = (
                f"🏪 *Магазин {store_id}: {store_name}*\n"
                "══════════════════════════\n"
                f"*Ответственный:* {store['specialist']}\n"
                f"*Телефон:* {store['spec_phone']}\n\n"
                "*Нажмите «◀️ Назад к списку» для выбора другого магазина*"
            )
            
            safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("◀️ Назад к списку"))
            safe_send_message(message.chat.id, f"❌ Магазин с ID {store_id} не найден.", reply_markup=markup)
    
    except Exception as e:
        print(f"❌ Ошибка в show_store_info: {e}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад к списку"))
        safe_send_message(message.chat.id, f"❌ Ошибка: {str(e)}", reply_markup=markup)

# 🔴 ОСНОВНЫЕ ФУНКЦИИ НАВИГАЦИИ
@bot.message_handler(func=lambda m: m.text == "◀️ Назад в админ-панель")
def back_to_admin_panel(message):
    try:
        if message.from_user.id != ADMIN_ID:
            return
        admin_panel(message)
    except Exception as e:
        print(f"❌ Ошибка в back_to_admin_panel: {e}")

@bot.message_handler(func=lambda m: m.text == "◀️ Назад к списку")
def back_to_store_list(message):
    try:
        show_stores(message)
    except Exception as e:
        print(f"❌ Ошибка в back_to_store_list: {e}")

@bot.message_handler(func=lambda m: m.text in ["◀️ Назад в меню", "◀️ Назад"])
def back_to_menu(message):
    try:
        send_welcome(message)
    except Exception as e:
        print(f"❌ Ошибка в back_to_menu: {e}")

# 🔴 ОБРАБОТКА ДРУГИХ КОМАНД
@bot.message_handler(commands=['myid'])
def show_my_id(message):
    try:
        user_id = message.from_user.id
        response = f"🆔 Ваш Telegram ID: `{user_id}`\n\n"
        
        if user_id == ADMIN_ID:
            response += "✅ Вы администратор этого бота!"
        else:
            response += "👤 Вы обычный пользователь"
        
        safe_send_message(message.chat.id, response, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в show_my_id: {e}")

@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в меню"))
        
        help_text = (
            "📚 *ПОМОЩЬ ПО БОТУ*\n\n"
            "*Основные команды:*\n"
            "• /start — Главное меню\n"
            "• /myid — Узнать свой Telegram ID\n"
            "• /all — Показать все магазины\n"
            "• /help — Эта справка\n\n"
            "*Навигация:*\n"
            "• Используйте кнопки для выбора действий\n"
            "• Кнопка «◀️ Назад» возвращает на предыдущий шаг\n"
            "• Кнопка «◀️ Назад в меню» возвращает в главное меню\n\n"
            "💡 *Совет:* Чаще оставляйте обратную связь — это помогает улучшать бота!"
        )
        
        if message.from_user.id == ADMIN_ID:
            help_text += "\n\n👑 *Администратору доступно:*\n"
            help_text += "• Админ-панель в главном меню\n"
            help_text += "• Добавление и редактирование магазинов\n"
            help_text += "• Экспорт данных и просмотр статистики"
        
        safe_send_message(message.chat.id, help_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в help_command: {e}")

@bot.message_handler(commands=['all'])
def show_all_stores(message):
    try:
        if not stores:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("◀️ Назад в меню"))
            safe_send_message(message.chat.id, "📭 Список магазинов пуст.", reply_markup=markup)
            return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("◀️ Назад в меню"))
        
        response = "🏪 *Все магазины:*\n\n"
        
        for store_id, store_info in stores.items():
            response += f"*{store_id}. {store_info['name']}*\n"
            response += f"👤 {store_info['specialist']}\n"
            response += f"📱 {store_info['spec_phone']}\n"
            response += "─" * 25 + "\n"
        
        safe_send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка в show_all_stores: {e}")

# Запускаем бот
if __name__ == "__main__":
    try:
        set_bot_commands()  # Устанавливаем команды меню
        print("=" * 60)
        print("🤖 БОТ СЛУЖБЫ ОХРАНЫ ТРУДА ЗАПУЩЕН")
        print(f"👑 Админ ID: {ADMIN_ID}")
        print(f"🏪 Магазинов в базе: {len(stores)}")
        print("📱 Версия: 1.2 (с защитой от ошибок сети)")
        print("🌐 Flask сервер запущен для keep-alive")
        print("=" * 60)
        
        # Очищаем webhook перед запуском polling
        try:
            bot.remove_webhook()
            print("✅ Webhook очищен")
        except:
            pass
        
        time.sleep(3)  # Задержка 3 секунды
        
        # Запускаем polling БЕЗ skip_pending
        print("🔄 Запуск polling с новым токеном...")
        bot.polling(
            none_stop=True,
            interval=2,
            timeout=30
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
    except Exception as e:
        print(f"\n⚠️ Ошибка: {e}")
        print(traceback.format_exc())
        print("⏳ Перезапуск через 10 секунд...")
        time.sleep(10)
        # Автоперезапуск
        os.execv(sys.executable, ['python'] + sys.argv)
