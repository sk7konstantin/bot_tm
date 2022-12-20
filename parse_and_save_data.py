import requests
from bs4 import BeautifulSoup
import json
import re
import os

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

# Пути к корню проекта
root_path = os.path.abspath('./')

# Проверяем есть ли папка с данными, если нет, создаем
if not os.path.isdir(os.path.join(root_path, 'data')):
    os.mkdir(os.path.join(root_path, 'data'))
    data_path = os.path.join(root_path, 'data')
else:
    data_path = os.path.join(root_path, 'data')

#todo Ссылка на Уголовный кодекс
CRIMINAL_CODE_URL = 'https://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=CdV4tw&base=LAW&n=422137&cacheid=9DBAF61D07DA57EFF418EEBAA965B517&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-10000&current=0&_=1663266700172&rnd=CdV4tw'

#todo Ссылка на Гражданский процессуальный кодекс
CIVIL_PROCEDURE_CODE_URL = 'http://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=TNXDnw&base=LAW&n=433425&cacheid=484B32FD66A020B60B993E8BD3D0243E&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-10000&current=0&content=text&_=1670792664830&rnd=TNXDnw'

#todo Ссылка на Граждаское законодательство
CIVIL_LEGISLATION_URL_1 = 'https://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=TNXDnw&base=LAW&n=410706&cacheid=CFAA35FACDA087F4BF98C528A104296B&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-100000&_=1670792664830&rnd=TNXDnw'
CIVIL_LEGISLATION_URL_2 = 'https://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=TNXDnw&base=LAW&n=377025&cacheid=CDB05BDCE6FC123B56C82C74004E474A&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-100000&_=1670792664830&rnd=TNXDnw'
CIVIL_LEGISLATION_URL_3 = 'http://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=TNXDnw&base=LAW&n=389129&cacheid=1A03A443216608682A51A1414DCAFC8E&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-100000&_=1670792664830&rnd=TNXDnw'
CIVIL_LEGISLATION_URL_4 = 'http://www.consultant.ru/cons/cgi/online.cgi?req=doc&rnd=TNXDnw&base=LAW&n=428378&cacheid=42EE5BBCCE08081FA3DCBA2BB6A2DB97&mode=rubr&docaccess=ALWAYS&content=zone&zone=0-100000&_=1670792664830&rnd=TNXDnw'

file_name_criminal = 'CRIMINAL_CODE'
file_name_civil_procedure = 'CIVIL_PROCEDURE_CODE'
file_name_civil_legislation = 'CIVIL_LEGISLATION'

file_name_and_url_list = [(file_name_criminal, [CRIMINAL_CODE_URL]), 
                (file_name_civil_procedure, [CIVIL_PROCEDURE_CODE_URL]),
                (file_name_civil_legislation, [CIVIL_LEGISLATION_URL_1, CIVIL_LEGISLATION_URL_2, CIVIL_LEGISLATION_URL_3, CIVIL_LEGISLATION_URL_4])]


def get_data(url, file_name):
    '''
        Получаем данные от сайта и сохраняем их в json файл
    '''
    r = requests.get(url=url, headers=HEADERS)

    with open(f'{file_name}_dirty.json', 'w', encoding='utf-8') as f:
        json.dump(r.json(), f, ensure_ascii=False, indent=4)


def parse_json(url, file_name, param_write='w'):
    '''
        param_write - Параметр записи в файл
        Считываем json файл
        Находим все элементы по нужному классу
        Пробегаясь в цикле, записываем данные в словарь: 
            где ключ - название статьи,
            значение - информация по статье
        После сохраняем получившийся словарь в json файл
    '''
    # with open(f'{file_name}_dirty.json', 'r', encoding='utf-8') as f:
    #     data = json.loads(f.read())
    
    data = requests.get(url=url, headers=HEADERS).json()

    bs = BeautifulSoup(data['text']['content'], 'html.parser')
    elements = bs.find_all('div', {'class': 'U'})

    articles_dict = {}
    counter_list = []

    current_article = ''

    for i in range(9, len(elements)):
        text_element = elements[i].text.strip()

        if re.match('Статья [0-9]*', text_element) or i == len(elements)-1:
            for j in counter_list:
                if elements[j].text.strip():
                    try:
                        articles_dict[current_article].append(elements[j].text.strip())
                    except Exception:
                        pass
            current_article = text_element
            articles_dict[current_article] = []

            counter_list = []
            continue

        counter_list.append(i)

    if param_write == 'a':
        return articles_dict
    else:
        with open(f'{os.path.join(data_path, file_name)}.json', param_write, encoding='utf-8') as f:
            json.dump(articles_dict, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    for file_name, url_list in file_name_and_url_list:
        if len(url_list) > 1:
            articles_dict_all = []
            for url_item in url_list:
                # get_data(url_item, file_name)
                articles_dict_all.append(parse_json(url_item, file_name, 'a'))

            with open(f'{os.path.join(data_path, file_name)}.json', 'w', encoding='utf-8') as f:
                json.dump(articles_dict_all, f, ensure_ascii=False, indent=4)
        else:
            # get_data(url_list[0], file_name)
            parse_json(url_list[0], file_name)