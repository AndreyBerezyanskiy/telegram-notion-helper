from telegram import Update
from telegram.ext import ContextTypes
from notion_api import create_notion_task

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відповідь на команду /start."""
    chat_id = update.message.chat_id
    # Додаємо await перед асинхронним викликом
    await context.bot.send_message(chat_id=chat_id, text="Привіт! Я твій помічник з Notion. Щоб додати завдання введи /add та потім текст питання, якщо потрібно додати посилання на вірш, додай ; та потім вірш")

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Додає нове завдання в Notion через команду /add."""
    chat_id = update.message.chat_id
    input_text = ' '.join(context.args)  # Отримуємо весь текст завдання

    # Розділяємо текст на опис завдання і вірш
    if ';' in input_text:
        task_description, task_verse = input_text.split(';', 1)  # Розділяємо за першим входженням `;`
        task_description = task_description.strip()  # Очищаємо пробіли
        task_verse = task_verse.strip()  # Очищаємо пробіли
    else:
        task_description = input_text.strip()
        task_verse = None

    if task_description:
        # Створюємо завдання в Notion
        notion_response = create_notion_task(task_description, task_verse)
        if notion_response:
            await context.bot.send_message(chat_id=chat_id, text=f"Завдання '{task_description}' додано в Notion!")
        else:
            await context.bot.send_message(chat_id=chat_id, text="Не вдалося додати завдання в Notion.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Будь ласка, надай опис завдання після команди /add.")

