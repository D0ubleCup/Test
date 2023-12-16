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
    await message.answer('Для начала выберите соц. сеть', reply_markup=kb.choise_social_network)
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
    if message.text:
        if len(message.text) < 15895:
            await state.update_data(post_text = message.text)
            await message.answer('Хорошо, отправьте фотографию для поста')
            await state.set_state(Data.photo)
        else:
            await message.answer('Текст слишком большой, пишлите текст покороче')
    else:
        await message.answer('Пришлите текст для поста!')
        

@dp.message(Data.photo)
async def posting_photo(message: Message, state: FSMContext):
    if message.photo:
        global Api_Vk
        file_id = message.photo[-1].file_id
        await state.update_data(photo = f'{file_id}')
        await bot.download(file=file_id, destination=f'content/{file_id}.jpg')

        data = await state.get_data()
        Api_Vk = VKapi(data=data)
        await state.clear()

        await message.answer('Желаете ли вы добавить дополнительные пункты к посту?\nВыберите настройку которую хотите добавить или запостите запись', reply_markup=kb.add_settings_choise)
    else: 
        await message.answer('Пришлите фото для поста!')
    

    

@dp.message(F.text)
async def add_settings_choise(message: Message):
    if Api_Vk.ready_post():
        if message.text == 'Доступ к записи':
            await message.reply('Желаете ли вы ограничить доступ к записи', reply_markup=kb.friends_only)
        elif message.text == 'Закрыть комментарии':
            await message.reply('Желаете ли вы закрыть комментарии', reply_markup=kb.comments)
        elif message.text == 'Опубликовать':
            await message.reply('Публикация', reply_markup=kb.rmk)
            answer = Api_Vk.work_api()
            Api_Vk.__del__()
            await message.reply(text=answer, reply_markup=kb.rmk)

        elif message.text == 'Инфо о посте':
            data = Api_Vk.get_data()
            yes = 'да'
            no = 'нет'
            await message.reply(text = f'Текст: {data["message"]} \nфото: {data["attachments"]} \nТолько для друзей: {yes if data["friends_only"]==True else no} \nЗакрыть комментарии: {yes if data["close_comments"]==True else no}')

        elif message.text =='Отменить действия':
            await message.reply('Все действия успешно удалены, нажмите /go, что бы начать заново', reply_markup=kb.start_keyboard)
            Api_Vk.__del__()
    else:
        await message.reply('Я вас не понимаю')

@dp.callback_query(F.data=='friends_only_yes')
async def friends_only_yes(callback: CallbackQuery):
    Api_Vk.add_settings({'friends_only':True})
    await callback.message.answer('Параметр "Только для друзей" включен', reply_markup=kb.add_settings_choise)

@dp.callback_query(F.data=='friends_only_no')
async def friends_only_no(callback: CallbackQuery):
    Api_Vk.add_settings({'friends_only':False})
    await callback.message.answer('Параметр "Только для друзей" выключен')

@dp.callback_query(F.data=='comments_yes')
async def comments_yes(callback: CallbackQuery):
    Api_Vk.add_settings({'close_comments':True})
    await callback.message.answer('Параметр "закрыть комментарии" включен')

@dp.callback_query(F.data=='comments_no')
async def comments_no(callback: CallbackQuery):
    Api_Vk.add_settings({'close_comments':False})
    await callback.message.answer('Параметр "закрыть комментарии" выключен')



    




