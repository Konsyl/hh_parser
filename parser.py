import requests
from bs4 import BeautifulSoup
from lxml import html
from extensions import check_exp, check_skills, find_requirements, strs_in_it

class vacancy_parser():

    def __init__(self, text_of_src):
        self.text_os_src = text_of_src

    def get_page(self, number):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        }

        url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text={0}&page={1}'

        request_url = url.format(self.text_os_src, number)
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text)
        else:
            return None

    def get_vacancies(self):

        soup = get_page(self, 1)

        vacancies = soup.find_all('a', attrs={'class': 'bloko-link HH-LinkModifier'})

        sat_vacancies = []

        for vac in vacancies:
            requirements = find_requirements(vac)
            if not requirements:
                continue
            elif not check_skills(requirements):
                continue
            elif not check_exp(vac):
                continue
            else:
                sat_vacansies.append(vac.get('href'))
        return sat_vacansies

text_of_src = """python AND (junior OR (NOT middle AND NOT senior)) AND (удалённая OR удалённо)"""