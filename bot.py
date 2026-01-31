import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import telegram_info

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Telegram Info Bot\n\n"
        "Gunakan:\n"
        "/info username\n\n"
        "Contoh:\n"
        "/info telegram"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Contoh: /info telegram")
        return

    username = context.args[0].replace("@", "")
    data = telegram_info(username)

    if "error" in data:
        await update.message.reply_text(f"❌ {data['error']}")
        return

    msg = "🔍 *Telegram Profile Info*\n\n"
    for k, v in data.items():
        msg += f"*{k}:* {v}\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()