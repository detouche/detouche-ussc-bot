from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import types, Bot, F
from aiogram.filters import Text

from loader import rt

from keyboards.reply.admin_create_session import admin_create_session
from keyboards.inline.confirmation_candidate_name import get_keyboard_confirmation
from keyboards.reply.admin_successful_creation import admin_delete_session

from states.admin_confirmation_candidate_name import ConfirmationCandidateName, CandidateName
from states.admin_session import AdminSession

from database.connection_db import get_profile_list, get_session_info

from handlers.custom_handlers.role import admin_command
from handlers.custom_handlers.admin_choosing_actions_profile import creating_pdf


@rt.message(Text('Создать сессию'))
@admin_command
async def create_session(message: types.Message, state: FSMContext, *args, **kwargs):
    users_id = get_session_info(4)
    await state.clear()
    if message.chat.id not in users_id:
        await message.answer(text=f'Введите ФИО кандидата',
                             reply_markup=admin_create_session)
        await state.set_state(AdminSession.name)
    else:
        await message.answer(text=f'Ошибка: У вас уже есть созданная сессия.\n'
                                  f'Закончите ее, чтобы начать новую',
                             reply_markup=admin_delete_session)


@rt.message(AdminSession.name)
async def session_candidate_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    candidate_name = await state.get_data()
    await state.clear()
    await message.answer(text=f'Вы уверены?',
                         reply_markup=get_keyboard_confirmation())
    await CandidateName.set_data(state, data={'candidate_name': candidate_name['name']})


@rt.callback_query(ConfirmationCandidateName.filter(F.action == 'confirmat_cand_name'))
async def get_confirmation(callback: CallbackQuery, callback_data: ConfirmationCandidateName, state: FSMContext,
                           bot: Bot):
    data = await state.get_data()
    confirmation = callback_data.confirmation
    candidate_name = data['candidate_name']
    if confirmation:
        await callback.message.delete()
        await callback.message.answer(f"Выберите профили для {candidate_name.title()}")
        await profile_list_session(message=callback.message, bot=bot)
        await state.set_state(AdminSession.profile_number)
    else:
        await callback.message.delete()
        await create_session(message=callback.message, state=state)


async def profile_list_session(message: types.Message, bot: Bot):
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', data_profile_list)))
    await message.answer(text=f'Список всех имеющихся профилей:\n\n'
                              f'{data_profile_list}')
    await creating_pdf(bot, message)
