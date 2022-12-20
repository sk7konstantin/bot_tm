from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from data_base import func_with_DB

from create_bot import dp


# @dp.message_handler(Text(equals ='Показать кол-во оставшихся статей'))
async def get_length_db(message: types.Message):
    name_file = f'{message.from_id}.db'
    dict_name_tables = {
                    'УК РФ': 'criminal_code', 
                    'ГК РФ': 'civil_legislation', 
                    'ГПК РФ': 'civil_procedure_code'
    }

    for name_code, name_table in dict_name_tables.items():
        result = func_with_DB.length_db(name_file, name_table)
        await message.answer(f'Кол-во оставшихся статей в {name_code} - {result}')


# Регистрация хэндлеров
def register_handler_user(dp: Dispatcher):
    dp.register_message_handler(get_length_db, Text(equals ='Показать кол-во оставшихся статей'))
    