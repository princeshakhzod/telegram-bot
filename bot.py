from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update

# Botning tokeni
TOKEN = '7484845792:AAHnvpREXZ5xaLEkTpEOMM22wAPlpmnulLI'

# Yo'lovchilar va haydovchilar ma'lumotlarini saqlash uchun lug'at
passenger_data = {}

# Tugmalarni yaratish
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
        [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
        [InlineKeyboardButton("Buxoro", callback_data='Buxoro')],
        [InlineKeyboardButton("Telefon raqamingizni kiriting", callback_data='get_phone')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Iltimos, manzilni tanlang:', reply_markup=reply_markup)

# Telefon raqamni olish
async def get_phone(update: Update, context):
    await update.message.reply_text('Telefon raqamingizni kiriting (masalan, +998XXXXXXXXX):')

# Telefon raqamini saqlash
async def phone_handler(update: Update, context):
    phone = update.message.text
    user_id = update.message.from_user.id
    if user_id not in passenger_data:
        passenger_data[user_id] = {}
    passenger_data[user_id]['phone'] = phone
    await update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

# Manzilni tanlash
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    # Manzilni tanlash
    if query.data in ['Toshkent', 'Samarqand', 'Buxoro']:
        if user_id not in passenger_data:
            passenger_data[user_id] = {}
        passenger_data[user_id]['destination'] = query.data
        await query.edit_message_text(text=f"Manzil: {query.data}. Telefon raqamingizni kiriting:")
    elif query.data == 'get_phone':
        await query.edit_message_text(text="Telefon raqamingizni kiriting:")

# Taksi haydovchisi uchun manzilni so'rash
async def driver_start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
        [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
        [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Haydovchi sifatida manzilni tanlang:', reply_markup=reply_markup)

# Botni ishga tushirish
def main():
    # Application yaratish
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, phone_handler))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("driver", driver_start))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
