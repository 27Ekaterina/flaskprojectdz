import requests
from pickle import dump, load
import pprint
from functions import *
import json
import time
import sqlite3
from sqlite3 import connect



def parce(vacancy, where, area=113):

    try:
        database = []

        for page in range(0, 3):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'text': vacancy if where == 'all' else f'NAME:{vacancy}' if where == 'name' else f'DESCRIPTION:{vacancy}',
                'where': where,
                'area': 113 if area == 'all' else '1' if area == 'Moscow' else '2',
                'page': page
            }
            result = requests.get(url, params=params).json()
            time.sleep(0.25)
            database.append(result)

        av_zp = average_salary(database)
        count_vacancies = result['found']

        vacancies_url = []
        skills = []

        for page in database:
            items = page['items']
            for vacancie in items:
                url = vacancie['url']
                result1 = requests.get(url).json()
                vacancies_url.append(result1)

        for i in vacancies_url:
            skill = i['key_skills']
            if skill != None:
                skills.append(skill)

        skills2 = []
        for skill in skills:
            for i in skill:
                for key, value in i.items():
                    skills2.append(value)

        key_skills_list = []
        for skill in skills2:
            if skill not in key_skills_list:
                key_skills_list.append(skill)

        key_skills = {}
        for item in skills2:
            # если он уже там есть
            if item in key_skills:
                # то мы его увеличиваем на 1
                key_skills[item] += 1
            else:
                # а если еще там нет
                # то мы его записываем со значением 1
                key_skills[item] = 1
        result = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

        sum_of_values = sum(key_skills.values())
        key_skills2 = dict(map(lambda v: [v[0], round(v[1] / sum_of_values * 100, 1)], key_skills.items()))
        key_skills2_sort = sorted(key_skills2.items(), key=lambda x: x[1], reverse=True)

        result_file = {"count_vacancies": count_vacancies,
                       "average salary": round(av_zp),
                       "key_skills": key_skills_list[0:4],
                       "key_skills_count": result[0:4],
                       "key_skills_percent": key_skills2_sort[0:4]}

        # Заполнение таблиц базы данных результатами поиска

        conn = sqlite3.connect('hhsqlite.sqlite')
        cur = conn.cursor()
        # проверка наличия региона/условия поиска/вакансии в таблицах
        rest = cur.execute('select id from area where area.regioncode = ?', (params['area'],)).fetchone()
        condition = cur.execute('select id from where_search where where_search.name = ?',
                                (params['where'],)).fetchone()
        vacancies = cur.execute('select id from words where words.word = ?', (vacancy,)).fetchone()
        if not rest:
            # добавление строки в таблицу регионов.
            cur.execute('insert into area values (null, ?)', (params['area'],))
        if not condition:
            # добавление строки в таблицу условий поиска.
            cur.execute('insert into where_search values (null, ?)', (params['where'],))
        if not vacancies:
            # добавление строки в таблицу вакансий.
            cur.execute('insert into words values (null, ?)', (vacancy,))

        for item in result_file["key_skills_percent"]:
            slills_list = cur.execute('select * from skills where skills.name = ?', (item[0],)).fetchone()
            if not slills_list:
            # добавление строки в таблицу требований к соискателям.
                cur.execute('insert into skills values (null, ?)', (item[0],))

        # заполнение итоговой таблицы
        cur.execute('select id from words where words.word = ?', (vacancy,))
        result = cur.fetchone()
        word_id = result[0]
        cur.execute('select id from area where area.regioncode = ?', (params['area'],))
        result = cur.fetchone()
        area_id = result[0]
        condition = cur.execute('select id from where_search where where_search.name = ?', (params['where'],))
        result = cur.fetchone()
        where_search_id = result[0]
        for item in result_file["key_skills_percent"]:
            cur.execute('select id from skills where skills.name = ?', (item[0],))
            result = cur.fetchone()
            skill_id = result[0]
            cur.execute('select * from wordskills as ws where ws.id_word = ? and ws.id_skill = ? and ws.id_area = ? and ws.id_where_search = ?', (word_id, skill_id, area_id, where_search_id))
            res = cur.fetchone()
            if not res:
                cur.execute('insert into wordskills values (?, ?, ?, ?, ?, ?, ?)', (word_id, skill_id, area_id, where_search_id, count_vacancies, av_zp, item[1]))
            else:
                 cur.execute('update wordskills as ws set count = ?, sellary = ?, percent = ? where ws.id_word = ? and ws.id_skill = ? and ws.id_area = ? and ws.id_where_search = ?', (count_vacancies, av_zp, item[1], word_id, skill_id, area_id, where_search_id))

        conn.commit()

        FILE_NAME = "hhparsing.json"
        with open(FILE_NAME, 'w') as f:
            json.dump(result_file, f)

        return result_file
    except ZeroDivisionError:
        print('Данных нет.\n Измените условия поиска')

if __name__=='__main__':
    pprint.pprint(parce('python', 'name', 'SPB'))