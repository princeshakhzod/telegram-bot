from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update

# Botning tokeni
TOKEN = '7484845792:AAHnvpREXZ5xaLEkTpEOMM22wAPlpmnulLI'

# Yo'lovchilar va haydovchilar ma'lumotlarini saqlash uchun lug'at
passenger_data = {}
driver_data = {}

# Tugmalarni yaratish
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Yo'lovchi", callback_data='passenger')],
        [InlineKeyboardButton("Haydovchi", callback_data='driver')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Siz haydovchimisiz yoki Yo\'lovchi?', reply_markup=reply_markup)

# Yo'lovchi yoki Haydovchi tanlanganda
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == 'passenger':
        # Yo'lovchi bo'lsa, manzilni tanlash
        keyboard = [
            [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
            [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
            [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)

    elif query.data == 'driver':
        # Haydovchi bo'lsa, manzilni tanlash
        keyboard = [
            [InlineKeyboardButton("Toshkent", callback_data='Toshkent_driver')],
            [InlineKeyboardButton("Samarqand", callback_data='Samarqand_driver')],
            [InlineKeyboardButton("Buxoro", callback_data='Buxoro_driver')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)

    elif query.data in ['Toshkent', 'Samarqand', 'Buxoro']:
        # Yo'lovchi uchun manzilni tanlash
        passenger_data[user_id] = {'category': 'passenger', 'destination': query.data}
        await query.edit_message_text(text=f"Manzil: {query.data}. Telefon raqamingizni kiriting:")

    elif query.data in ['Toshkent_driver', 'Samarqand_driver', 'Buxoro_driver']:
        # Haydovchi uchun manzilni tanlash
        driver_data[user_id] = {'category': 'driver', 'destination': query.data}
        await query.edit_message_text(text=f"Manzil: {query.data}.")

# Telefon raqamni olish
async def get_phone(update: Update, context):
    phone = update.message.text
    user_id = update.message.from_user.id

    # Yo'lovchi uchun telefon raqamini saqlash
    if user_id in passenger_data:
        passenger_data[user_id]['phone'] = phone
        await update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')
        
        # Manzilga qarab, haydovchiga telefon raqamini yuborish
        destination = passenger_data[user_id]['destination']
        for driver_id, driver_info in driver_data.items():
            if driver_info['destination'] == destination:
                driver_phone = passenger_data[user_id]['phone']
                # Faqat haydovchiga telefon raqamini yuborish
                await update.message.reply_text(f"Haydovchi uchun telefon raqami: {driver_phone}")

    # Haydovchi uchun telefon raqamini saqlash (bu yerda raqam so'ralmaydi)
    if user_id in driver_data:
        driver_data[user_id]['phone'] = phone  # Haydovchi telefon raqami faqat saqlanadi
        await update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')
        
        # Manzilga qarab, yo'lovchiga telefon raqamini yuborish
        destination = driver_data[user_id]['destination']
        for passenger_id, passenger_info in passenger_data.items():
            if passenger_info['destination'] == destination:
                passenger_phone = driver_data[user_id]['phone']
                # Faqat yo'lovchiga telefon raqamini yuborish
                await update.message.reply_text(f"Yo'lovchi uchun telefon raqami: {passenger_phone}")

# Botni ishga tushirish
def main():
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone))
    application.add_handler(CallbackQueryHandler(button))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
