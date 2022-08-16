import requests

def average_salary(database):
    for v in database:
        vacancy = v['items']
        n = 0
        n1 = 0
        sum_zp_min = 0
        sum_zp_max = 0
        min_zp = 0
        max_zp = 0
        vacancies_with_zp_min = 0
        vacancies_with_zp_max = 0
        for i in vacancy:
            if i['salary'] != None:
                zp = i['salary']
                if zp['from'] != None:
                    n += 1
                    sum_zp_min += zp['from']
                if zp['to'] != None:
                    n1 += 1
                    sum_zp_max += zp['to']
        min_zp += sum_zp_min
        max_zp += sum_zp_max
        vacancies_with_zp_min += n
        vacancies_with_zp_max += n1
    av_zp = (min_zp / vacancies_with_zp_min + max_zp / vacancies_with_zp_max) / 2
    return av_zp