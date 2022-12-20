import sqlite3 as sq
import json
import os


path_dir_data = os.path.abspath('data')
path_dir_data_base = os.path.abspath('data_base')

def create_table_after_first_start(name_file, name_table):
    '''Создаем БД при первом запуске.
        Считываем данные из json файла,
        после переводим значения объекта в строку,
        записываем в БД    
    '''
    with open(os.path.join(path_dir_data, f'{name_table.upper()}.json'), encoding='utf-8') as f:
        data = json.load(f)

    with sq.connect(f'{os.path.join(path_dir_data_base, f"{name_file}.db")}') as con:
        cur = con.cursor()

        cur.execute(f'''
            create table if not exists {name_table} (
                article_id integer primary key autoincrement,
                name_article text,
                description_article text
            )
        ''')

        for key in data:
            cur.execute(f'''
                insert into {name_table} (name_article, description_article)
                values (?,?)
            ''', (key, ' -- '.join(data[key])))


    print(f'БД - {name_table} - created')


def create_table(new_name_file, name_file, name_table):
    with sq.connect(f'{os.path.join(path_dir_data_base, f"{name_file}")}') as con:
        cur = con.cursor()
        cur.execute(f'''
            select * from {name_table} 
        ''')
        data = cur.fetchall()

    with sq.connect(os.path.join(path_dir_data_base, f"{new_name_file}")) as con:
        cur = con.cursor()
        cur.execute(f'''
            create table if not exists {name_table} (
                article_id integer primary key autoincrement,
                name_article text not null,
                description_article text
            )
        ''')
        cur.executemany(f'''
            insert into {name_table} (article_id, name_article, description_article)
            values (?,?,?)
        ''', data)


def drop_table(name_file, name_table):
    try:
        with sq.connect(os.path.join(path_dir_data_base, name_file)) as con:
            cur = con.cursor()

            cur.execute(f'''
                DROP TABLE if exists {name_table}
            ''')
    except Exception:
        print('БД нет')


def delete_from(name_file, name_table, target_id):
    with sq.connect(os.path.join(path_dir_data_base, name_file)) as con:
        cur = con.cursor()

        cur.execute(f'''
            delete from {name_table}
            where article_id = {target_id}
        ''')


def length_db(name_file, name_table):
    with sq.connect(os.path.join(path_dir_data_base,name_file)) as con:
        cur = con.cursor()

        cur.execute(f'''
            select * from {name_table}
        ''')
        result = cur.fetchall()

        return len(result)

def query_select(name_file, name_table, search_number):
    with sq.connect(os.path.join(path_dir_data_base, name_file)) as con:
        cur = con.cursor()

        cur.execute(f'''
            select * from {name_table}
            where name_article like 'Статья {search_number}.%'
        ''')
        return cur.fetchall()


def get_choice_article(name_file, name_table):
    with sq.connect(os.path.join(path_dir_data_base,name_file)) as con:
        cur = con.cursor()
        cur.execute(f'''
            select * from {name_table}
            order by random()
            limit 1
        ''')
        result = cur.fetchall()

        return result





    
