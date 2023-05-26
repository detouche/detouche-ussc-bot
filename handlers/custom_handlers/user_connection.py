from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from keyboards.reply.user_connection import user_connection

from database.connection_db import user_register, auth_validation, user_rename, user_has_active_session, \
    get_session_code, get_user_name_for_id

from states.user_info import User

from handlers.custom_handlers.role import user_command


async def user_start(message: types.Message, state: FSMContext, bot: Bot, url_code: str = None):
    await state.clear()
    user_id = message.from_user.id
    authorized = auth_validation(user_id)
    if authorized:
        if user_has_active_session(user_id):
            await message.answer(text=f'Предупреждение: Вы не закончили оценку прошлой сессии')
            await state.set_state(User.connection_code)
            await state.update_data(connection_code=get_session_code(user_id))

            from handlers.custom_handlers.user_start_grading import user_start_grading_info
            await user_start_grading_info(message, state, bot)
        else:
            if url_code is None:
                user_name = get_user_name_for_id(user_id)
                await message.answer(text=f'Здравствуйте, {user_name.title()}')
                await message.answer(text=f'Введите код сессии или перейдите по ссылке от администратора',
                                     reply_markup=user_connection)
                await bot.send_document(chat_id=message.chat.id, document=FSInputFile(r"photo\manual.jpg"))
                await state.set_state(User.connection_code)
            else:
                await bot.send_document(chat_id=message.chat.id, document=FSInputFile(r"photo\manual.jpg"))
                await state.set_state(User.connection_code)
                await state.update_data(connection_code=url_code)
                from handlers.custom_handlers.user_start_grading import user_start_grading_info
                await user_start_grading_info(message, state, bot)
    else:
        await message.answer("Здравствуйте! Введите свое ФИО, чтобы зарегистрироваться")
        await state.set_state(User.name)


@rt.message(User.name)
async def user_enter_name(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id
    await message.answer(f"Вы успешно зарегистрировались, {user_data['name']}!")
    await state.clear()
    user_register(user_id, user_data['name'])
    await user_start(message=message, state=state, bot=bot)


@rt.message(Text('Изменить имя'))
@user_command
async def user_want_rename(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer("Как вас перезаписать?")
    await state.set_state(User.rename)


@rt.message(User.rename)
async def user_enter_rename(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(rename=message.text)
    user_data = await state.get_data()
    current_id = message.from_user.id
    await message.answer(f"Вы перезаписаны, {user_data['rename'].title()}!")
    await state.clear()
    user_rename(current_id, user_data['rename'])
    await user_start(message=message, state=state, bot=bot)
