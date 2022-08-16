import requests
from pickle import dump, load
import pprint
from functions import *
import json
import time

def parce(vacancy, where, area=113):

    try:
        database = []

        for page in range(0, 3):
            url = 'https://api.hh.ru/vacancies'
            params = {
                'text': vacancy if where == 'all' else f'NAME:{vacancy}' if where == 'name' else f'DESCRIPTION:{vacancy}',
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

        FILE_NAME = "hhparsing.json"
        with open(FILE_NAME, 'w') as f:
            json.dump(result_file, f)

        return result_file
    except ZeroDivisionError:
        print('Данных нет.\n Измените условия поиска')

if __name__=='__main__':
    pprint.pprint(parce('python', 'name', 'SPB'))