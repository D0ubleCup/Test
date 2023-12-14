from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove


rmk = ReplyKeyboardRemove()

start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/go')]], resize_keyboard=True)

choise_social_network = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='вк'),
    KeyboardButton(text='vs.ru')],
    [KeyboardButton(text='dzen'),
    KeyboardButton(text='linkedin')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')

add_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='да', callback_data='add_settings')],
    [InlineKeyboardButton(text='нет', callback_data='123')]
])

add_settings_choise = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Доступ к записи')],
    [KeyboardButton(text='Закрыть комментарии')],
], resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')

friends_only = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='да', callback_data='friends_only_yes')],
    [InlineKeyboardButton(text='нет', callback_data='friends_only_no')]
])

