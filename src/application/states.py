from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    personal_data = State()
    surname = State()
    name = State()
    patronymic = State()
    birth_date = State()
    phone = State()
    email = State()
    gender = State()
    region_by_text = State()
    region_by_button = State()
    city = State()

