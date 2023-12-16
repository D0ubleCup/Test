from aiogram.fsm.state import StatesGroup, State

class Data(StatesGroup):
    network: str = State() #str
    post_text: str = State() #str
    photo: str = State() #str

