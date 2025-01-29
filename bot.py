from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import CallbackContext

# Botning tokeni
TOKEN = '7484845792:AAHnvpREXZ5xaLEkTpEOMM22wAPlpmnulLI'

# Yo'lovchilar va haydovchilar ma'lumotlarini saqlash uchun lug'at
passenger_data = {}
driver_data = {}

# Botni boshlashda foydalanuvchidan haydovchi yoki yo'lovchi tanlashini so'rash
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Yo'lovchi", callback_data='passenger')],
        [InlineKeyboardButton("Haydovchi", callback_data='driver')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Siz haydovchimisiz yoki Yo\'lovchi?', reply_markup=reply_markup)

# Haydovchi yoki Yo'lovchi tanlanganida
async def button(update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if query.data == 'passenger':
        # Yo'lovchi tanlangan
        passenger_data[user_id] = {}
        keyboard = [
            [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
            [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
            [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)
    
    elif query.data == 'driver':
        # Haydovchi tanlangan
        driver_data[user_id] = {}
        keyboard = [
            [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
            [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
            [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)

# Manzilni tanlash
async def destination_button(update, context):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    destination = query.data
    if user_id in passenger_data:
        # Yo'lovchi uchun manzilni saqlash
        passenger_data[user_id]['destination'] = destination
        await query.edit_message_text(text=f"Manzil: {destination}. Telefon raqamingizni kiriting:")
    
    elif user_id in driver_data:
        # Haydovchi uchun manzilni saqlash
        driver_data[user_id]['destination'] = destination
        await query.edit_message_text(text=f"Manzil: {destination}.")

# Telefon raqamni olish va saqlash
async def phone_handler(update, context):
    phone = update.message.text
    user_id = update.message.from_user.id
    
    if user_id in passenger_data:
        # Yo'lovchi uchun telefon raqamini saqlash
        passenger_data[user_id]['phone'] = phone
        await update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

        # Manzilga qarab, haydovchilarga telefon raqamini yuborish
        destination = passenger_data[user_id]['destination']
        for driver_id, driver_info in driver_data.items():
            if driver_info['destination'] == destination:
                driver_phone = passenger_data[user_id]['phone']
                # Haydovchiga telefon raqamini yuborish
                await context.bot.send_message(driver_id, f"Yo'lovchi uchun telefon raqami: {driver_phone}")
    
    elif user_id in driver_data:
        # Haydovchi uchun telefon raqamini saqlash (faqat saqlanadi, yuborilmaydi)
        driver_data[user_id]['phone'] = phone
        await update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

        # Yo'lovchiga telefon raqamini yuborish
        destination = driver_data[user_id]['destination']
        for passenger_id, passenger_info in passenger_data.items():
            if passenger_info['destination'] == destination:
                passenger_phone = driver_data[user_id]['phone']
                # Yo'lovchiga telefon raqamini yuborish
                await context.bot.send_message(passenger_id, f"Haydovchi uchun telefon raqami: {passenger_phone}")

# Botni ishga tushirish
def main():
    application = Application.builder().token(TOKEN).build()

    # Komandalar va handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CallbackQueryHandler(destination_button))
    application.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, phone_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
