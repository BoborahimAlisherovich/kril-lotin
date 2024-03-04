from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

user_button = ReplyKeyboardMarkup(
    keyboard=[
        
        [KeyboardButton(text="Murojat yo'llash"), KeyboardButton(text="Mening murojatlarim")],

        [KeyboardButton(text="Biz haqimizda")]

    
    ],
    resize_keyboard=True,
    input_field_placeholder="Menu"
)
