import requests
from bs4 import BeautifulSoup
from lxml import html


def strs_in_it(it, strs):
    for st in strs:
        if (st.lower() in it.lower()):
            return True
    return False


strs_for_requirements = ['Требования', 'от кандидата',
                         'Необходимо', 'Пожелания',
                         'Требуем', 'Ждем', 'Ожидания',
                         'потребуются']

strs_for_satisfy = ['django', 'flask', 'rest']

strs_for_exp = ['не требуется', '1-3 года', '3-6 лет']


def find_requirements(vac):
    vac_response = requests.get(vac.get('href'), headers=headers)
    vac_body = BeautifulSoup(vac_response.text)

    description = vac_body.find('div', attrs={'data-qa': 'vacancy-description'})
    if not description:
        return None
    else:
        req_tags = description.find_all(['p', 'ui', 'strong'])
        for p in req_tags:
            if strs_in_it(it=p.text, strs=strs_for_requirements):

                if '-' in p.text:
                    return [req.lower() for req in p.text.split('-')[1:]]

                requirements = p.find_next_sibling()
                # print(requirements)
                if not requirements:
                    # print(p)
                    return None
                if requirements.name == 'ul' or requirements.name == 'ol':
                    # print('стандартный список')
                    return [i.text.lower() for i in requirements.find_all('li')]

    return None


def check_skills(requirements):
    for req in requirements:
        for skill in strs_for_satisfy:
            if skill in req:
                return True
    return False


def check_exp(vac):
    vac_response = BeautifulSoup(requests.get(vac.get('href'), headers=headers).text)
    return vac_response.find('span', attrs={'data-qa': 'vacancy-experience'}).text.lower() in strs_for_exp