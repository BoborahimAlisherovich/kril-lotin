from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,CallbackQuery
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts
from states.register import Register
from keyboard_buttons.main import user_button
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboard_buttons.register import contact_button
import time 
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message:Message,state:FSMContext):   
    try:
        telegram_id = message.from_user.id
        ids = [id[0] for id in await db.all_users_id()]
        if telegram_id in ids:
            await message.answer(text="Assalomu alaykum",reply_markup=user_button)
        else:
            await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz\n Ro'yhatdan o'tish uchun Ismingizni kiriting ")
            await state.set_state(Register.first_name)          
    except:
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz\n Ro'yhatdan o'tish uchun Ismingizni kiriting ")
        await state.set_state(Register.first_name)

@dp.message(F.text,Register.first_name)
async def first_name_register(message:Message,state:FSMContext):
    first_name = message.text
    
    await state.update_data(first_name=first_name)
    await state.set_state(Register.last_name)
    await message.answer(text="familyangizni kriting")


@dp.message(F.text,Register.last_name)
async def last_name_register(message:Message,state:FSMContext):
    last_name = message.text
    await state.update_data(last_name = last_name)
    await state.set_state(Register.phone_number)

    await message.answer(text="Kontakt yuboring",reply_markup=contact_button)


@dp.message(F.contact,Register.phone_number)
async def phone_number_register(message:Message,state:FSMContext):
    data = await state.get_data()
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id

    await state.clear()
    await db.add_user(telegram_id=telegram_id,first_name=first_name,last_name=last_name,phone_number=phone_number)
    await message.answer(text="Siz muvaffaqiyatli tarzda ro'yhatdan o'tdingiz\nBotimizdan foydalanishingiz mumkin",reply_markup=user_button)




@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)





#Admin panel uchun
@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = await db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.5)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()




@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))



async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="data/main.db")
    db.create_table_users()
    db.create_table_tasks()
    await set_default_commands(bot)
    await dp.start_polling(bot)
    setup_middlewares(dispatcher=dp, bot=bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())