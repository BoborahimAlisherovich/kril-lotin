from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()