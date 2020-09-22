from parser import VacancyParser
from celery import Celery
from celery import task
from extensions import send_telegram
from worker import app

text_of_src = """python AND (junior OR (NOT middle AND NOT senior)) AND (удалённая OR удалённо)"""
skills = ['django', 'flask', 'rest', 'git', 'python']


parser = VacancyParser(text_of_src, skills, 1)



@app.task
def start_parsing():
    for i in range(1, 5):
        result = parser.get_vacancies(percent=0.0, page=i)
        for vac in result:
            send_telegram(text=vac)


@app.task
def start_status():
    send_telegram(text='work is up')
