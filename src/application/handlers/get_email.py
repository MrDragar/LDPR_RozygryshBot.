import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.fio)
async def get_fio(message: types.Message, state: FSMContext):
    fio = message.text
    logger.debug(f"Got fio {fio}")
    await state.update_data(fio=fio)
    await state.set_state(RegistrationStates.phone)
    await message.reply("Введите ваш номер телефона")
