from loader import rt
from aiogram import F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_grading_competencies import user_grading_get_keyboard, grade_text_converter
from keyboards.inline.user_grade import user_grade_get_keyboard
from keyboards.reply.user_end_grading import user_end_grading

from handlers.custom_handlers.role import user_command, get_role

from states.user_grading_competence import UserGrading, UserGrade, CompetenceSessionInfo

from database.connection_db import get_current_comp_desc_session, get_current_comp_name_session, \
    get_current_comp_grade_session, transform_grade_current_comp, active_session


@rt.message(Text("Начать оценку"))
@user_command
async def user_grading_process(message: Message, state: FSMContext, *args, **kwargs):
    if active_session(message.chat.id):
        await message.answer(text=f'Вы начали оценку сессии!',
                             reply_markup=user_end_grading)
        await user_grading_get_keyboard(message)
    else:
        await message.answer(text=f'<b>Ошибка:</b> Данная сессия уже закончена!')
        await get_role(message, state)


@rt.callback_query(UserGrading.filter(F.action == 'assessment'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserGrading, state: FSMContext):
    competence_id = callback_data.competence_id
    competence_name = get_current_comp_name_session(competence_id)
    competence_desc = get_current_comp_desc_session(competence_id)
    competence_grade = get_current_comp_grade_session(competence_id)
    competence_grade = grade_text_converter(int(competence_grade))
    await callback.message.edit_text(text=f"<b>Название компетенции:</b> {competence_name.capitalize()}\n"
                                          f"<b>Описание компетенции:</b> {competence_desc.capitalize()}\n\n"
                                          f"Текущая оценка: <b>{competence_grade}</b>",
                                     reply_markup=user_grade_get_keyboard())
    await CompetenceSessionInfo.set_data(state, data={'competence_id': competence_id})


@rt.callback_query(UserGrade.filter(F.action == 'assessment_grade'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserGrade, state: FSMContext,
                                 bot: Bot):
    data = await state.get_data()
    await state.clear()
    competence_id = data['competence_id']
    grade = callback_data.grade
    transform_grade_current_comp(competence_id, grade)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await user_grading_get_keyboard(callback.message)
