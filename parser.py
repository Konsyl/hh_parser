import requests
from bs4 import BeautifulSoup
from extensions import check_exp, check_skills, find_requirements, strs_in_it


class VacancyParser:
    def __init__(self, text_of_src, skills, exp):
        self.text_os_src = text_of_src
        self.skills = skills

        if exp == 0:
            strs_for_exp = ['не требуется']
        elif exp == 1:
            strs_for_exp = ['не требуется', '1-3 года']
        else:
            strs_for_exp = ['не требуется', '1-3 года', '3-6 лет']

        self.exp = strs_for_exp

        self.headers = {
            'User-Agent':
                """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36""",
        }

    def get_page(self, number):

        url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text={0}&page={1}'

        request_url = url.format(self.text_os_src, number)
        response = requests.get(request_url, headers=self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text)
        else:
            return None

    def get_vacancies(self, percent=0.3, page=1):

        soup = self.get_page(1)

        vacancies = soup.find_all('a', attrs={'class': 'bloko-link HH-LinkModifier'})

        sat_vacancies = []

        for vac in vacancies:
            requirements = find_requirements(vac, self.headers)
            if not requirements:
                continue
            elif not check_skills(requirements, self.skills, percent):
                continue
            elif not check_exp(vac, self.exp, self.headers):
                continue
            else:
                sat_vacancies.append(vac.get('href'))
        return sat_vacancies
