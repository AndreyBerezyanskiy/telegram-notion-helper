import json
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from bot_handlers import start, add_task

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEVELOPMENT = os.getenv('DEVELOPMENT')
bot = Bot(token=TELEGRAM_TOKEN)

application = Application.builder().token(TELEGRAM_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("add", add_task))

if DEVELOPMENT:
    if __name__ == '__main__':
        print("Bot is running")
        application.run_polling()
else:
    def lambda_handler(event, context):
        """AWS Lambda entry point."""

        if event.get("httpMethod") == "POST":
            update = Update.de_json(json.loads(event["body"]), bot)

            application.update_queue.put(update)
            return {
                'statusCode': 200,
                'body': json.dumps('Success')
            }

        return {
            'statusCode': 400,
            'body': json.dumps('Only POST method is supported')
        }
