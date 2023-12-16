from aiogram import Router

from aiogram import  F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from tools import keyboards as kb
from tools.FSLclasses import Data

router = Router()



@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! \nДля продолжения введите команду /go', reply_markup= kb.start_keyboard)


@router.message(F.text == '/go')
async def go_work(message: Message, state: FSMContext):
    await message.answer('Для начала выберите соц. сеть', reply_markup=kb.choise_social_network)
    await state.set_state(Data.network)
    