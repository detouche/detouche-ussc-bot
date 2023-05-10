from loader import rt
from aiogram import F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_grading_competencies import user_grading_get_keyboard, grade_text_converter
from keyboards.inline.user_grade import user_grade_get_keyboard
from keyboards.reply.user_end_grading import user_end_grading

from handlers.custom_handlers.role import user_command

from states.user_grading_competence import UserGrading, UserGrade, CompetenceSessionInfo

from database.connection_db import get_current_comp_desc_session, get_current_comp_name_session, \
    get_current_comp_grade_session, transform_grade_current_comp


@rt.message(Text("Начать оценку"))
@user_command
async def user_grading_process(message: Message, *args, **kwargs):
    await message.answer(text=f'Вы начали оценку сессии',
                         reply_markup=user_end_grading)
    await user_grading_get_keyboard(message)


@rt.callback_query(UserGrading.filter(F.action == 'assessment'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserGrading, state: FSMContext):
    comp_id = callback_data.competence_id
    comp_name = get_current_comp_name_session(comp_id)
    comp_desc = get_current_comp_desc_session(comp_id)
    comp_grade = get_current_comp_grade_session(comp_id)
    comp_grade = grade_text_converter(int(comp_grade))
    await callback.message.edit_text(text=f"Название компетенции: {comp_name}\n\n"
                                          f"Описание компетенции: {comp_desc}\n\n"
                                          f"Текущая оценка: {comp_grade}",
                                     reply_markup=user_grade_get_keyboard())
    await CompetenceSessionInfo.set_data(state, data={'competence_id': comp_id})


@rt.callback_query(UserGrade.filter(F.action == 'assessment_grade'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserGrade, state: FSMContext,
                                 bot: Bot):
    data = await state.get_data()
    await state.clear()
    comp_id = data['competence_id']
    grade = callback_data.grade
    transform_grade_current_comp(comp_id, grade)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await user_grading_get_keyboard(callback.message)
