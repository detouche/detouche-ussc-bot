from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from loader import rt
from aiogram import types, F
from aiogram.filters import Text

from keyboards.reply.admin_create_session import admin_create_session, admin_choice_profile
from keyboards.inline.confirmation_candidate_name import get_keyboard_confirmation
# from handlers.custom_handlers.role import admin_command
from states.admin_confirmation_candidate_name import ConfirmationCandidateName, CandidateName
from states.admin_session import AdminSession


@rt.message(Text('Создать сессию'))
# @admin_command
async def create_session(message: types.Message, state: FSMContext):
    await message.answer(text=f'Введите ФИО кандидата',
                         reply_markup=admin_create_session)
    await state.set_state(AdminSession.name)
    print(await state.set_state(AdminSession.name), AdminSession.name)


@rt.message(AdminSession.name)
async def session_candidate_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    candidate_name = await state.get_data()
    print(candidate_name)
    await state.clear()
    await message.answer(text=f'Вы уверены?',
                         reply_markup=get_keyboard_confirmation())
    await CandidateName.set_data(state, data={'candidate_name': candidate_name['name']})


@rt.callback_query(ConfirmationCandidateName.filter(F.action == 'confirmat_cand_name'))
async def get_confirmation(callback: CallbackQuery, callback_data: ConfirmationCandidateName, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    confirmation = callback_data.confirmation
    candidate_name = data['candidate_name']
    if confirmation:
        await callback.message.delete()
        await callback.message.answer(f"Выберите профили для {candidate_name}",
                                      reply_markup=admin_choice_profile)
    else:
        await create_session(callback.message, state)
