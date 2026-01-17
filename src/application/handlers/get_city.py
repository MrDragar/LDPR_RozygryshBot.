import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.city)
async def get_city(message: types.Message, state: FSMContext,
                   user_service: IUserService, log_chat: str):
    city = message.text
    if not city:
        return
    logger.debug(f"Got city {city}")
    if not city or len(city) < 2:
        return await message.reply(
            "Введите название вашего города или населённого пункта")

    data = await state.get_data()
    surname = data['surname']
    name = data['name']
    patronymic = data['patronymic']
    birth_date = data['birth_date']
    phone = data['phone']
    email = data['email']
    region = data['region']
    gender = data['gender']

    if await user_service.is_user_exists(message.from_user.id):
        return await message.reply(f"Вы уже зарегистрировались.")

    user = await user_service.create_user(
        message.from_user.id, message.from_user.username,
        surname, name, patronymic, birth_date, phone, region, email, gender, city
    )
    await state.clear()
    await message.reply(
        f"Поздравляем, вы успешно зарегистрированы.\n",
        parse_mode="HTML"
    )
    await message.answer_sticker(types.FSInputFile('docs/sokol_like.webp'))
    await message.bot.send_message(chat_id=log_chat, text=f"""
Новый пользователь {'@' + user.username if user.username else '<нет username>'} зарегистрировался.
ФИО: {user.surname} {user.name} {user.patronymic}
Пол: {user.gender}
Дата рождения: {user.birth_date.strftime('%d.%m.%Y')}
Почта: {user.email}
Номер телефона: {user.phone_number}
Регион: {user.region}
Город: {user.city}

Номер участника: Б{user.id}
""")
