import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.surname)
async def get_surname(message: types.Message, state: FSMContext):
    if not message.text:
        return
    surname = message.text.strip()
    if not surname:
        await message.reply("Пожалуйста, введите фамилию")
        return

    logger.debug(f"Got surname: {surname}")
    await state.update_data(surname=surname)
    await state.set_state(RegistrationStates.name)
    await message.reply("Отлично! Теперь введите ваше имя")


@router.message(RegistrationStates.name)
async def get_name(message: types.Message, state: FSMContext):
    if not message.text:
        return
    name = message.text.strip()
    if not name:
        await message.reply("Пожалуйста, введите имя")
        return

    logger.debug(f"Got name: {name}")
    await state.update_data(name=name)
    await state.set_state(RegistrationStates.patronymic)
    await message.reply(
        "Введите ваше отчество (если нет отчества, отправьте прочерк '-' или слово 'нет')")


@router.message(RegistrationStates.patronymic)
async def get_patronymic(message: types.Message, state: FSMContext):
    if not message.text:
        return
    patronymic = message.text.strip()

    if patronymic.lower() in ['-', 'нет', 'нету', 'отсутствует', '']:
        patronymic = None

    logger.debug(f"Got patronymic: {patronymic}")
    await state.update_data(patronymic=patronymic)
    await state.set_state(RegistrationStates.birth_date)
    await message.reply(
        "Введите вашу дату рождения в формате ДД.ММ.ГГГГ\n(например, 15.05.1990)")
