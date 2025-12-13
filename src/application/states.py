from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    personal_data = State()
    fio = State()
    phone = State()
    email = State()
    gender = State()
    region_by_text = State()
    region_by_button = State()
    city = State()
