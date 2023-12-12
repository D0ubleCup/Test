from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()



@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!')

