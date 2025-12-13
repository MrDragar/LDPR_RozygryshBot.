import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.city)
async def get_city(message: types.Message, state: FSMContext,
                   user_service: IUserService):
    city = message.text
    logger.debug(f"Got city {city}")
    if not city or len(city) < 2:
        return await message.reply(
            "Введите название вашего города или населённого пункта")

    data = await state.get_data()
    fio = data['fio']
    phone = data['phone']
    email = data['email']
    region = data['region']
    gender = data['gender']
    user = await user_service.create_user(
        message.from_user.id, message.from_user.username,
        fio, phone, region, email, gender, city
    )
    await state.clear()
    await message.reply(
        f"Поздравляем, вы успешно зарегистрированы.\n"
        f"Ваш уникальный номер - {user.id}. Дата финала - 31.12.2025",
        parse_mode="HTML"
    )
