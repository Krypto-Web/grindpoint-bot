import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ================== CONFIG ==================
BOT_TOKEN = "8622829038:AAFhGZy_xQAPTEHrw_4Cs_hTE_vcX2HqHgM"
ADMIN_ID = 7997697892          # Your Telegram user ID

GROUP_LINK = "https://t.me/+NJLTREq5F6E4NWE0"
REGISTER_LINK = "https://grindpoint.com.ng/register"

# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = """Hello 👋

Welcome on board!

To get started:
1. Join our Telegram group for updates and support
2. Create your free account on Grindpoint

Once you’re registered, you can start completing tasks and earning real Naira.

If you need any help, just tap the button below.

Welcome to the Grindpoint family 🔥"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("📝 Create Free Account", url=REGISTER_LINK)],
        [InlineKeyboardButton("🆘 I Need Help", callback_data="need_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "need_help":
        # Reply to user
        await query.message.reply_text(
            "Okay, I’ve received your request ✅\n\n"
            "A human support agent will get back to you shortly. Please describe your problem."
        )

        # Notify Admin
        user = query.from_user
        username = f"@{user.username}" if user.username else "No username"
        text = (
            f"🆘 *New Support Request*\n\n"
            f"From: {user.full_name}\n"
            f"Username: {username}\n"
            f"User ID: `{user.id}`\n\n"
            f"They clicked *I Need Help*"
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text,
            parse_mode="Markdown"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any normal text message"""
    user = update.effective_user
    message_text = update.message.text

    # Always send welcome + buttons if it's a new conversation style message
    if message_text.lower() in ["hi", "hello", "hey", "good morning", "good evening", "start"]:
        await start(update, context)
        return

    # Treat other messages as support requests
    await update.message.reply_text(
        "Thank you for your message.\n\n"
        "A human support agent will get back to you shortly. Please wait."
    )

    # Notify Admin
    username = f"@{user.username}" if user.username else "No username"
    text = (
        f"💬 *New Message from User*\n\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"User ID: `{user.id}`\n\n"
        f"Message:\n{message_text}"
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Grindpoint Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
