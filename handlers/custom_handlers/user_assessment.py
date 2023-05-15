from loader import rt
from aiogram import F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_grading_competencies import user_grading_get_keyboard, grade_text_converter
from keyboards.inline.user_grade import user_grade_get_keyboard

from handlers.custom_handlers.role import user_command, get_role

from states.user_grading_competence import UserGrading, UserGrade, CompetenceSessionInfo
from states.user_info import User

from database.connection_db import get_current_comp_desc_session, get_current_comp_name_session, \
    get_current_comp_grade_session, transform_grade_current_comp, active_session, get_session_code


@rt.message(Text("Приступить к оцениванию"))
@user_command
async def user_grading_process(message: Message, state: FSMContext, *args, **kwargs):
    if active_session(message.chat.id):
        await message.answer(text=f'Вы начали оценку сессии!')
        await user_grading_get_keyboard(message)
    else:
        await message.answer(text=f'Ошибка: Данная сессия уже закончена!')
        await get_role(message, state)


@rt.callback_query(UserGrading.filter(F.action == 'assessment'))
async def user_grading_info(callback: CallbackQuery, callback_data: UserGrading, state: FSMContext):
    competence_id = callback_data.competence_id
    competence_name = get_current_comp_name_session(competence_id)
    competence_desc = get_current_comp_desc_session(competence_id)
    competence_grade = get_current_comp_grade_session(competence_id)
    competence_grade = grade_text_converter(int(competence_grade))
    await callback.message.edit_text(text=f"Название компетенции: {competence_name.capitalize()}\n"
                                          f"Описание компетенции: {competence_desc.capitalize()}\n\n"
                                          f"Текущая оценка: {competence_grade}",
                                     reply_markup=user_grade_get_keyboard())
    await CompetenceSessionInfo.set_data(state, data={'competence_id': competence_id})


@rt.callback_query(UserGrade.filter(F.action == 'assessment_grade'))
async def user_successfully_grading(callback: CallbackQuery, callback_data: UserGrade, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    competence_id = data['competence_id']
    grade = callback_data.grade
    transform_grade_current_comp(competence_id, grade)
    await callback.message.delete()
    await user_grading_get_keyboard(callback.message)


@rt.callback_query(Text(startswith='stop_grading'))
async def delete_admin_finish(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    if active_session(callback.message.chat.id):
        await callback.message.answer(text=f'Проверка кандидата завершена!\n'
                                           f'Вы можете изменить поставленные оценки, нажав '
                                           f'Приступить к оцениванию')
        user_id = callback.message.chat.id
        connection_code = get_session_code(user_id)
        await state.set_state(User.connection_code)
        await state.update_data(connection_code=connection_code)

        from handlers.custom_handlers.user_start_grading import user_start_grading_info
        await user_start_grading_info(callback.message, state)
    else:
        await callback.message.answer(text=f'Ошибка: Данная сессия уже закончена!')
        await get_role(callback.message, state)
