from aiogram import types, Dispatcher
from data_base import func_with_DB
from create_bot import dp
import os
from keyboards import kb_user


# Название файлов где лежат данные статей
name_files = ['civil_legislation', 'civil_procedure_code', 'criminal_code']

# Пути к директориям
path_dir_data = os.path.abspath('data')
path_dir_data_base = os.path.abspath('data_base')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    name_file = f'{message.from_id}.db'
    base_name_file = 'all_articles.db'

    if not os.path.isfile(os.path.join(path_dir_data_base, f"{user_id}.db")):
        for name_table in name_files:
            func_with_DB.create_table(name_file, base_name_file, name_table)
        await message.answer(f'<b>База данных создана! \nудачного пользования!</b>', reply_markup=kb_user)
    else:
        await message.answer(f'<b>Для Вас БД уже есть, можете продолжать пользоваться!</b>', reply_markup=kb_user)
    
    

def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])