from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Botning tokeni
TOKEN = '7484845792:AAHnvpREXZ5xaLEkTpEOMM22wAPlpmnulLI'

# Yo'lovchilar va haydovchilar ma'lumotlarini saqlash uchun lug'at
passenger_data = {}

# Tugmalarni yaratish
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
        [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
        [InlineKeyboardButton("Buxoro", callback_data='Buxoro')],
        [InlineKeyboardButton("Telefon raqamingizni kiriting", callback_data='get_phone')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Iltimos, manzilni tanlang:', reply_markup=reply_markup)

# Telefon raqamni olish
def get_phone(update, context):
    update.message.reply_text('Telefon raqamingizni kiriting (masalan, +998XXXXXXXXX):')

# Telefon raqamini saqlash
def phone_handler(update, context):
    phone = update.message.text
    user_id = update.message.from_user.id
    if user_id not in passenger_data:
        passenger_data[user_id] = {}
    passenger_data[user_id]['phone'] = phone
    update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

# Manzilni tanlash
def button(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    
    # Manzilni tanlash
    if query.data in ['Toshkent', 'Samarqand', 'Buxoro']:
        if user_id not in passenger_data:
            passenger_data[user_id] = {}
        passenger_data[user_id]['destination'] = query.data
        query.edit_message_text(text=f"Manzil: {query.data}. Telefon raqamingizni kiriting:")
    elif query.data == 'get_phone':
        query.edit_message_text(text="Telefon raqamingizni kiriting:")

# Taksi haydovchisi uchun manzilni so'rash
def driver_start(update, context):
    keyboard = [
        [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
        [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
        [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Haydovchi sifatida manzilni tanlang:', reply_markup=reply_markup)

# Botni ishga tushirish
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~filters.command, phone_handler))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("driver", driver_start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
