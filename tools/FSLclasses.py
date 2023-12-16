from aiogram.fsm.state import StatesGroup, State

class Data(StatesGroup):
    network = State() #str
    post_text = State() #str
    photo = State() #str

