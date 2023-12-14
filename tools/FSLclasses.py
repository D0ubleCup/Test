from aiogram.fsm.state import StatesGroup, State

class Data(StatesGroup):
    network = State() #str
    post_text = State() #str
    photo = State() #str
    # add_settings = State() #bool
    # friends_only = State() #bool
    # close_comments = State() #bool
    # tags = State()
    
