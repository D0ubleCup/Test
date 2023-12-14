from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os

from tools import keyboards as kb
from tools.FSLclasses import Data
from APIclasses.BaseAPIrequest import VKapi

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()




@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать! \nДля продолжения введите команду /go', reply_markup= kb.start_keyboard)


@dp.message(F.text == '/go')
async def go_work(message: Message, state: FSMContext):
    await message.answer(text='Для начала выберите соц. сеть', reply_markup=kb.choise_social_network)
    await state.set_state(Data.network)

@dp.message(Data.network, F.text.casefold().in_(['вк'])) 
async def network_chosen(message: Message, state: FSMContext): 
    await state.update_data(network=message.text) 
    await message.answer( text="Хорошо, теперь пришлите мне текст", reply_markup=kb.rmk) 
    await state.set_state(Data.post_text)

@dp.message(Data.network)
async def incorent_network(message: Message, state: FSMContext):
    await message.answer('Введите соц. сеть или выберите ее нажимая на кнопку (пока что доступен только vk)', reply_markup=kb.choise_social_network)
    

@dp.message(Data.post_text)
async def posting_text(message: Message, state: FSMContext):
    await state.update_data(post_text = message.text)
    await message.answer('Хорошо, отправьте фотографию для поста')
    await state.set_state(Data.photo)
    

@dp.message(Data.photo)
async def posting_photo(message: Message, state: FSMContext):
    global Api_Vk
    file_id = message.photo[-1].file_id
    await state.update_data(photo = file_id)
    await bot.download(file=file_id, destination=f'content/{file_id}.jpg')
    
    data = await state.get_data()
    Api_Vk = VKapi(data=data)
    await state.clear()


    await message.answer('Желаете ли вы добавить дополнительные пункты к посту(хэштеги, доступ, доступ к коментариям)', reply_markup=kb.add_settings)
    

    

@dp.callback_query(F.data == 'add_settings')
async def add_settings_fn(callback: CallbackQuery):
    await callback.message.answer('Выберите настройку которую хотите добавить', reply_markup=kb.add_settings_choise)

@dp.message(F.text)
async def add_settings_choise(message: Message):
    if message.text == 'Доступ к записи':
        await message.reply('Желаете ли вы ограничить доступ к записи', reply_markup=kb.friends_only)
    elif message.text == 'Закрыть комментарии':
        pass
    else:
        pass

@dp.callback_query(F.data=='friends_only_yes')
async def friends_only_yes(callback: CallbackQuery):
    Api_Vk.add_settings({'friends_only':True})
    print(Api_Vk.__dict__)
    print(Api_Vk._Api_VK__params)
@dp.callback_query(F.data=='friends_only_no')
async def friends_only_no(callback: CallbackQuery):
    Api_Vk.add_settings({'friends_only':False})
    await callback.message.answer('re,g')


    






