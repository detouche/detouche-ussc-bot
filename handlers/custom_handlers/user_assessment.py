from loader import rt
from aiogram import F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_assessment_competencies import user_assessment_get_keyboard, value_converter_text
from keyboards.inline.user_assessment_grade import user_assessment_grade_get_keyboard
from keyboards.reply.user_end_assessment import user_end_assessment

from handlers.custom_handlers.role import user_command

from states.user_assessment_comp import UserAssessment, UserAssessmentGrade, CompSessionInfo

from database.connection_db import get_current_comp_desc_session, get_current_comp_name_session, \
    get_current_comp_grade_session, transform_grade_current_comp


@rt.message(Text("Начать оценку"))
@user_command
async def user_assessment_process(message: Message, *args, **kwargs):
    await message.answer(text=f'Вы начали оценку сессии',
                         reply_markup=user_end_assessment)
    await user_assessment_get_keyboard(message)


@rt.callback_query(UserAssessment.filter(F.action == 'assessment'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserAssessment, state: FSMContext):
    comp_id = callback_data.comp_id
    comp_name = get_current_comp_name_session(comp_id)
    comp_desc = get_current_comp_desc_session(comp_id)
    comp_grade = get_current_comp_grade_session(comp_id)
    comp_grade = value_converter_text(int(comp_grade))
    await callback.message.edit_text(text=f"Название компетенции: {comp_name}\n\n"
                                          f"Описание компетенции: {comp_desc}\n\n"
                                          f"Текущая оценка: {comp_grade}",
                                     reply_markup=user_assessment_grade_get_keyboard())
    await CompSessionInfo.set_data(state, data={'comp_id': comp_id})


@rt.callback_query(UserAssessmentGrade.filter(F.action == 'assessment_grade'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: UserAssessmentGrade, state: FSMContext,
                                 bot: Bot):
    data = await state.get_data()
    await state.clear()
    comp_id = data['comp_id']
    grade = callback_data.grade
    transform_grade_current_comp(comp_id, grade)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await user_assessment_get_keyboard(callback.message)
