from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import CallbackContext

# Botning tokeni
TOKEN = '7484845792:AAHnvpREXZ5xaLEkTpEOMM22wAPlpmnulLI'

# Yo'lovchilar va haydovchilar ma'lumotlarini saqlash uchun lug'at
passenger_data = {}
driver_data = {}

# Botni boshlashda foydalanuvchidan haydovchi yoki yo'lovchi tanlashini so'rash
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Yo'lovchi", callback_data='passenger')],
        [InlineKeyboardButton("Haydovchi", callback_data='driver')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Siz haydovchimisiz yoki Yo\'lovchi?', reply_markup=reply_markup)

# Haydovchi yoki Yo'lovchi tanlanganida
def button(update, context):
    query = update.callback_query
    query.answer()

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
        query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)
    
    elif query.data == 'driver':
        # Haydovchi tanlangan
        driver_data[user_id] = {}
        keyboard = [
            [InlineKeyboardButton("Toshkent", callback_data='Toshkent')],
            [InlineKeyboardButton("Samarqand", callback_data='Samarqand')],
            [InlineKeyboardButton("Buxoro", callback_data='Buxoro')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Qayerga borasiz?", reply_markup=reply_markup)

# Manzilni tanlash
def destination_button(update, context):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    destination = query.data
    if user_id in passenger_data:
        # Yo'lovchi uchun manzilni saqlash
        passenger_data[user_id]['destination'] = destination
        query.edit_message_text(text=f"Manzil: {destination}. Telefon raqamingizni kiriting:")
    
    elif user_id in driver_data:
        # Haydovchi uchun manzilni saqlash
        driver_data[user_id]['destination'] = destination
        query.edit_message_text(text=f"Manzil: {destination}.")

# Telefon raqamni olish va saqlash
def phone_handler(update, context):
    phone = update.message.text
    user_id = update.message.from_user.id
    
    if user_id in passenger_data:
        # Yo'lovchi uchun telefon raqamini saqlash
        passenger_data[user_id]['phone'] = phone
        update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

        # Manzilga qarab, haydovchilarga telefon raqamini yuborish
        destination = passenger_data[user_id]['destination']
        for driver_id, driver_info in driver_data.items():
            if driver_info['destination'] == destination:
                driver_phone = passenger_data[user_id]['phone']
                # Haydovchiga telefon raqamini yuborish
                context.bot.send_message(driver_id, f"Yo'lovchi uchun telefon raqami: {driver_phone}")
    
    elif user_id in driver_data:
        # Haydovchi uchun telefon raqamini saqlash (faqat saqlanadi, yuborilmaydi)
        driver_data[user_id]['phone'] = phone
        update.message.reply_text(f'Sizning telefon raqamingiz saqlandi: {phone}')

        # Yo'lovchiga telefon raqamini yuborish
        destination = driver_data[user_id]['destination']
        for passenger_id, passenger_info in passenger_data.items():
            if passenger_info['destination'] == destination:
                passenger_phone = driver_data[user_id]['phone']
                # Yo'lovchiga telefon raqamini yuborish
                context.bot.send_message(passenger_id, f"Haydovchi uchun telefon raqami: {passenger_phone}")

# Botni ishga tushirish
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Komandalar va handlerlar
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CallbackQueryHandler(destination_button))
    dp.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, phone_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
