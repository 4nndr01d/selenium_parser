from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .models import Vacancy, Company


class HhParser:

    def get_pages_count(self):
        pagination_btn = self.driver.find_elements_by_css_selector("a.bloko-button[data-qa='pager-page']")
        if pagination_btn:
            return int(pagination_btn[-1].text)
        else:
            return 1

    def get_vacancies(self):
        vacancy_items = self.driver.find_elements_by_css_selector("div.vacancy-serp-item")
        for vacancy_item in vacancy_items:
            vacancy_url = vacancy_item.find_element_by_css_selector(
                'a[data-qa="vacancy-serp__vacancy-title"]').get_attribute("href")
            vacancy_data = self.parse_vacansy(self.get_vacancy_data, vacancy_url)
            self.set_vacancy_data(vacancy_data)
            return False

    def set_vacancy_data(self, data):
        if data['company_name']:
            company = self.set_company(data['company_name'])
        else:
            company = None
        vacancy = self.set_vacancy(data, company)

    def set_company(self, company_name):
        company = Company.objects.filter(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            company.save()
        return company

    def set_vacancy(self, vacancy_data, company):
        vacancy = Vacancy.objects.filter(vacancy_id=vacancy_data['vacancy_id']).first()
        if not vacancy:
            vacancy = Vacancy(name=vacancy_data['vacancy_name'],
                              description=vacancy_data['vacancy_description'],
                              salary=vacancy_data['vacancy_salary'],
                              address=vacancy_data['vacancy_address'],
                              url=vacancy_data['vacancy_url'],
                              vacancy_id=vacancy_data['vacancy_id'],
                              company=company
                              )
            vacancy.save()
        return vacancy

    def get_vacancy_data(self, vacancy_url):
        return {
            'vacancy_name': self.get_vacancy_name(),
            'vacancy_description': self.get_vacancy_description(),
            'vacancy_salary': self.get_vacancy_salary(),
            'skills': self.get_vacancy_skills(),
            'company_name': self.get_vacancy_company_name(),
            'vacancy_address': self.get_vacancy_address(),
            'vacancy_url': vacancy_url,
            'vacancy_id': self.get_vacancy_id()
        }

    def get_vacancy_address(self):
        try:
            address = self.driver.find_element_by_css_selector('span[data-qa="vacancy-view-raw-address"]').text
        except:
            address = ''
        return address

    def get_vacancy_id(self):
        return self.driver.find_element_by_css_selector('input[name=vacancyId]').get_attribute('value')

    def get_vacancy_company_name(self):
        return self.driver.find_element_by_css_selector('.vacancy-company__details a span span').text

    def get_vacancy_salary(self):
        return self.driver.find_element_by_css_selector('.vacancy-salary span').text

    def get_vacancy_skills(self):
        skills = []
        skills_btn = self.driver.find_elements_by_css_selector('div.bloko-tag.bloko-tag_inline')
        if (len(skills_btn)):
            for skill_btn in skills_btn:
                skills.append(skill_btn.text)
        return skills

    def get_vacancy_description(self):
        return self.driver.find_element_by_css_selector('div[data-qa="vacancy-description"]').text

    def get_vacancy_name(self):
        return self.driver.find_element_by_css_selector('div.vacancy-title h1').text

    def parse_vacansy(self, func, url):
        self.open_and_switch_new_tab(url)
        vacancy_data = func(url)
        self.close_and_switch_to_main_tab()
        return vacancy_data

    def open_and_switch_new_tab(self, url):
        self.driver.execute_script("window.open('')")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url)

    def close_and_switch_to_main_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def scrap(self, city):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        self.driver = driver
        driver.get("https://spb.hh.ru/search/vacancy?text=" + city)
        self.get_vacancies()
        driver.close()


if __name__ == '__main__':
    hh_parser = HhParser()
    hh_parser.scrap('python')
