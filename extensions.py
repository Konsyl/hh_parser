import requests
from bs4 import BeautifulSoup



def strs_in_it(it, strs):
    for st in strs:
        if (st.lower() in it.lower()):
            return True
    return False


strs_for_requirements = ['Требования', 'от кандидата',
                         'Необходимо', 'Пожелания',
                         'Требуем', 'Ждем', 'Ожидания',
                         'потребуются']


def find_requirements(vac, headers):
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


def check_skills(requirements, skills, per):
    count_max = len(requirements)
    count_temp = 0
    for req in requirements:
        for skill in skills:
            if skill in req:
                count_temp += 1
                if count_temp / count_max >= per:
                    return True
    return False


def check_exp(vac, exp, headers):
    vac_response = BeautifulSoup(requests.get(vac.get('href'), headers=headers).text)
    exp_from_vac = vac_response.find('span', attrs={'data-qa': 'vacancy-experience'}).text.lower()
    for item in exp:
        if exp_from_vac in exp:
            print('Да')
            return True
    return False

def send_telegram(text: str):
    token = "1217501559:"
    url = "https://api.telegram.org/bot"
    channel_id = "316852238"
    url += token
    method = url + "/sendMessage"

    r = requests.get(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        print(r)
        raise Exception("post_text error")