import logging
from aiogram import executor
from create_bot import dp
import os

from handlers import start,  user, search_articles, get_random_article, update_db
from data_base import func_with_DB

# Название файлов где лежат данные статей
name_files = ['civil_legislation', 'civil_procedure_code', 'criminal_code']

# Пути к директориям
path_dir_data = os.path.abspath('data')
path_dir_data_base = os.path.abspath('data_base')

# Фукнция запускается один раз в начале
# Провереяет, есть ли БД, если нет, то создаем и наполняем данными
async def on_startup(_):
    print('Бот вышел в онлайн')
    if os.path.isfile(os.path.join(path_dir_data_base, f'all_articles.db')):
        print('БД уже существует')
    else:
        for name_file in name_files:
            func_with_DB.create_table_after_first_start('all_articles', name_file)

start.register_handler_start(dp)
search_articles.register_handler_search_articles(dp)
get_random_article.register_handler_random_articles(dp)
update_db.register_handler_update_db(dp)
user.register_handler_user(dp)

if __name__ == '__main__': 
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)