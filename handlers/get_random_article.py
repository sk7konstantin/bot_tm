from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import user_kb
import re

from data_base import func_with_DB
from create_bot import dp


class FSMRandomArticle(StatesGroup):
    name_code = State()


# Начало диалога выбора кодекса где искать
# @dp.message_handler(Text(equals='Получить случайную статью'), state=None)
async def fsmrandom_start(message: types.Message):
    await FSMRandomArticle.name_code.set()
    await message.answer(f'<b>Выберите законодательство от куда получить статью...</b>', reply_markup=user_kb.kb_code_search)


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
async def get_random_article(message: types.Message, state: FSMContext):
    name_file = f'{message.from_id}.db'

    async with state.proxy() as data:
        data['name_code'] = message.text

    async with state.proxy() as data:
        code_dict = {
            'УК РФ': 'criminal_code',
            'ГК РФ': 'civil_legislation',
            'ГПК РФ': 'civil_procedure_code'
        }
        name_table = code_dict[data["name_code"]]

        result = func_with_DB.get_choice_article(name_file, name_table)

        if not result:
            await message.answer(f'❗️❗️Ошибка, попробуйте еще раз', reply_markup=user_kb.kb_user)

        for id, name, desc in result:
            desc = re.split(r' -- ', desc)
            result_text = ''
            for text in desc:
                if re.match(r'[0-9].', text):
                    result_text += "\n" + text
                else:
                    result_text += " " + text
                    
            try:
                await message.answer(f'✅{data["name_code"]}✅<b>{name}</b>')
                await message.answer(f"{result_text}", reply_markup=user_kb.kb_user)
            except Exception as ex:
                await message.answer(f'❗️❗️Ошибка, повторите запрос', reply_markup=user_kb.kb_user)

            func_with_DB.delete_from(name_file, name_table, id)
    await message.delete()
    await state.finish()


def register_handler_random_articles(dp: Dispatcher):
    dp.register_message_handler(fsmrandom_start, Text(equals='Получить случайную статью'), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(get_random_article, state=FSMRandomArticle.name_code)

