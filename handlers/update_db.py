from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import user_kb
import re

from data_base import func_with_DB
from create_bot import dp


class FSMUpdateDB(StatesGroup):
    name_code = State()


# Начало диалога выбора кодекса где искать
# @dp.message_handler(Text(equals='Обновить БД'), state=None)
async def fsmupdate_start(message: types.Message):
    await FSMUpdateDB.name_code.set()
    await message.answer(f'<b>Выберите БД которую нужно обновить...</b>', reply_markup=user_kb.kb_code_search)


# Выход из состояний
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(f'<b>OK</b>', reply_markup=user_kb.kb_user)
    await message.delete()


# Ловим ответ и пишем в словарь
# @dp.message_handler(state=FSMSearchCode.number_articles)
async def update_db(message: types.Message, state: FSMContext):
    name_file = f'{message.from_id}.db'
    base_name_file = 'all_articles.db'

    async with state.proxy() as data:
        data['name_code'] = message.text

    async with state.proxy() as data:
        code_dict = {
            'УК РФ': 'criminal_code',
            'ГК РФ': 'civil_legislation',
            'ГПК РФ': 'civil_procedure_code'
        }
        name_table = code_dict[data["name_code"]]


        func_with_DB.drop_table(name_file, name_table)
        func_with_DB.create_table(name_file, base_name_file, name_table)

        await message.answer(f'<b>БД обновлена!</b>', reply_markup=user_kb.kb_user)
    await message.delete()
    await state.finish()


def register_handler_update_db(dp: Dispatcher):
    dp.register_message_handler(fsmupdate_start, Text(equals='Обновить БД'), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(update_db, state=FSMUpdateDB.name_code)

