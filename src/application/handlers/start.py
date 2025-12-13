import logging

from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from src.application.keyboards.personal_data_keyboard import \
    get_personal_data_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
start_command_router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message()
@start_command_router.message(filters.CommandStart())
async def start(message: types.Message, user_service: IUserService, state: FSMContext):
    if await user_service.is_user_exists(message.from_user.id):
        logging.debug(f"User {message.from_user.id} already exists")
        return await message.reply(f"Вы уже зарегистрировались. Ваш номер: {message.from_user.id}")

    logging.debug(f"User {message.from_user.id} Start conversation")
    await message.reply(
        "Приветствие (текст в разработке)."
    )

    await message.reply("Для начала дайте согласие на обработку персональных данных", reply_markup=get_personal_data_keyboard())
    await state.set_state(RegistrationStates.personal_data)
