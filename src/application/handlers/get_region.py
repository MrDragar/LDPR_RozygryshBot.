import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.states import RegistrationStates
from src.application.callbacks import RegionCallback, RetryRegionCallback
from src.application.keyboards.region_keyborad import get_region_keyboard
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.region_by_text)
@router.message(RegistrationStates.region_by_button)
async def region_by_text(message: types.Message, state: FSMContext,
                         user_service: IUserService):
    logger.debug(f"Поиск региона {message.text}")
    if not message.text:
        return await message.reply("Укажите регион вашего проживания")
    regions = await user_service.get_similar_regions(message.text)
    logger.debug(f"Найденные регионы {regions}")
    await state.set_state(RegistrationStates.region_by_button)
    await message.reply(text='Выберите регион из списка',
                        reply_markup=get_region_keyboard(regions))


@router.callback_query(RetryRegionCallback.filter(),
                       RegistrationStates.region_by_button)
async def retry_region_callback(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)
    await state.set_state(RegistrationStates.region_by_text)
    return await query.message.reply("Укажите регион вашего проживания")


@router.callback_query(RegionCallback.filter(),
                       RegistrationStates.region_by_button)
async def region_by_button(query: types.CallbackQuery,
                           callback_data: RegionCallback, state: FSMContext,
                           user_service: IUserService):
    if await user_service.is_user_exists(query.from_user.id):
        address = await user_service.get_region_address(
            await user_service.get_user_region(query.from_user.id))
        logging.debug(f"User {query.from_user.id} already exists")
        return await query.reply(f"Вы уже успешно зарегистрировались\n\n"
                                 f"{address}\n"
                                 f"По указанному адресу вы сможете забрать свой подарок, а также получить полезную информацию."
                                 )
    await query.message.edit_reply_markup(reply_markup=None)
    region = callback_data.region
    logger.debug(f'Выбранный регион: {region}')
    address = await user_service.get_region_address(region)

    data = await state.get_data()
    fio = data['fio']
    phone = data['phone']
    email = data['email']
    await user_service.create_user(query.from_user.id, query.from_user.username,
                                   fio, phone, region, email)
    await state.clear()
    await query.message.reply(
        f"Поздравляем, вы успешно зарегистрированы.\n"
        f"{address}\n\n"
        f"По указанному адресу вы сможете забрать свой подарок, а также получить полезную информацию.",
        parse_mode="HTML"
    )
    await query.message.answer(
        """Пока вы ждёте, предлагаем провести время с пользой — на нашем <a href='https://t.me'>сайте</a> 
вы найдёте развивающие материалы для детей, доступные для мгновенного скачивания.""",
        parse_mode="HTML"
    )
