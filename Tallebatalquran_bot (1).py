
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime

# List to store usernames
user_list = []

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("أهلاً بكِ في بوت تحفيظ القرآن! ارسلي اليوزر الخاص بك لحجز الدور.")

# Handle username collection
def receive_user(update: Update, context: CallbackContext) -> None:
    global user_list
    current_time = datetime.datetime.now()
    # Allow user registration only during specific times
    if current_time.weekday() in [0, 1, 2] and current_time.hour == 17 and current_time.minute >= 30:
        username = update.message.from_user.username
        if username not in user_list:
            user_list.append(username)
            update.message.reply_text(f"تم تسجيل اليوزر: @{username}")
        else:
            update.message.reply_text("يوزرك مسجل بالفعل.")
    else:
        update.message.reply_text("الحجز غير متاح الآن.")

# Mention users handler
def mention_users(update: Update, context: CallbackContext) -> None:
    global user_list
    if user_list:
        mention_message = " ".join([f"@{user}" for user in user_list])
        update.message.reply_text(f"الأدوار: {mention_message}", parse_mode=ParseMode.MARKDOWN)
        user_list.clear()  # Clear the list after mentioning
    else:
        update.message.reply_text("لا يوجد أي طالبات مسجلات حالياً.")

# Main function to run the bot
def main():
    TOKEN = "7984915334:AAG7vfuF-A8JMB2dorp7la4aheWo8uWkoLw"
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_user))
    dispatcher.add_handler(CommandHandler("mention", mention_users))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
