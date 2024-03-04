from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

contact_button = ReplyKeyboardMarkup(
    keyboard=[[
    KeyboardButton(text="Kontakt yuborish", request_contact=True),]],
    resize_keyboard=True,
    input_field_placeholder="Kontakt yuborish tugmasini bosing"
)
