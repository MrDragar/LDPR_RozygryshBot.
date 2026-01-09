import logging

from aiogram import Router, types, F, filters
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.application.keyboards.admin.post_keyboard import get_post_keyboard
from src.application.states import PostsStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(filters.Command('cancel'))
@router.message(PostsStates.confirm, F.text.lower().strip() == 'отменить')
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Отмена рассылки", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(filters.Command('post'))
async def start_post_dialog_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите сообщение для рассылки")
    await state.set_state(PostsStates.get_message)


@router.message(PostsStates.get_message)
async def get_message_handler(message: types.Message, state: FSMContext):
    await message.answer("Подтвердите началу рассылки. Ваше сообщение:", reply_markup=get_post_keyboard())
    await message.bot.copy_message(message.chat.id, message.chat.id, message.message_id)
    await state.update_data(message_id=message.message_id)
    await state.set_state(PostsStates.confirm)


@router.message(PostsStates.confirm, F.text.lower().strip() == 'подтвердить')
async def confirm_post_handler(
        message: types.Message, state: FSMContext, user_service: IUserService
):
    users = await user_service.get_all_users()
    message_id = (await state.get_data())['message_id']
    await state.clear()
    await message.answer(f"Начинаю рассылку на {len(users)} пользователей", reply_markup=ReplyKeyboardRemove())
    success_count = 0
    for user in users:
        try:
            await message.bot.copy_message(user.id, message.chat.id, message_id)
            success_count += 1
        except Exception as e:
            logger.debug(e)
    await message.answer(f"Рассылка завершена. Отправлено "
                         f"успешно {success_count} сообщений из "
                         f"{len(users)}")


@router.message(PostsStates.confirm)
async def wait_confirm_post_handler(
        message: types.Message
):
    await message.answer("Подтвердите началу рассылки.", reply_markup=get_post_keyboard())