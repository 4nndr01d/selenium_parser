from __future__ import absolute_import, unicode_literals
import requests
from bs4 import BeautifulSoup as BS
from random import randint

from celery import shared_task

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
     'accept': '*/*'},
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'accept': '*/*'},
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'accept': '*/*'},
]

@shared_task(name='scrapping_work')
def scrapping_work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                vacancy_cards = main_div.find_all('div', attrs={'class': 'job-link'})
                for vacancy_card in vacancy_cards:
                    title = vacancy_card.find('h2')
                    href = title.a['href']
                    description = vacancy_card.p.text
                    company = 'No name'
                    company_title = (vacancy_card.find('div', attrs={'class': 'add-top-xs'}))
                    if company_title:
                        company = company_title.span.b.text
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': description,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language,
                                 })
            else:
                errors.append({'url': url, 'title': 'Main div does not funded'})
        else:
            errors.append({'url': url, 'title': 'Error! http code: ' + resp.status_code})
    print(jobs)
    # return jobs, errors