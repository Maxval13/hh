import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

HOST = 'https://hh.ru/search/vacancy'

def get_headers():
    return Headers(browser='chrome', os='win').generate()

params = {
    'no_magic': True,
    'L_save_area': True,
    'text': 'Python',
    'area': (1, 2),
    'search_period': 0,
    'items_on_page': 100

}

hh_html = requests.get(HOST, headers=get_headers(), params=params).text
soup = BeautifulSoup(hh_html, features='lxml')

content_list_tag = soup.find(id='a11y-main-content')
contents_tags = content_list_tag.find_all(class_='vacancy-serp-item__layout')

vacancys = []

for vacancy in contents_tags:
    name_company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    city = vacancy.select_one('.bloko-text[data-qa=vacancy-serp__vacancy-address]').text
    link_tag = vacancy.find('a', class_='serp-item__title')
    link = link_tag['href']
    hh_url = requests.get(link, headers=get_headers()).text
    soup_url = BeautifulSoup(hh_url, features='lxml')
    selary = soup_url.find(class_='bloko-header-section-2 bloko-header-section-2_lite').text
    user_content = soup_url.find(class_='g-user-content').text
    if ('Django' or 'django') in user_content and ('Flask' or 'flask') in user_content:
        vacancys.append({
            'Название компании': name_company.replace(u"\xa0", " "),
            'Город': city.replace(u"\xa0", " "),
            'з/п': selary.replace(u"\xa0", ""),
            'ссылка': link
        })


with open(r"vacancys.json", 'w', encoding='utf-8') as f:
    json.dump(vacancys, f, ensure_ascii=False, indent=2)




