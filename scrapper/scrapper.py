from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from .models import Vacancy, Company, Skill, Country, Area


class HhParser:
    def get_pages_count(self):
        pagination_btn = self.driver.find_elements_by_css_selector("a.bloko-button[data-qa='pager-page']")
        if pagination_btn:
            return int(pagination_btn[-1].text)
        else:
            return 1

    # todo отрефакторить методы get
    def get_vacancies(self):
        for vacancy_item in self.driver.find_elements_by_css_selector("div.vacancy-serp-item"):
            vacancy_url = vacancy_item.find_element_by_css_selector(
                'a[data-qa="vacancy-serp__vacancy-title"]').get_attribute("href")
            vacancy_data = self.parse_vacansy(self.get_vacancy_data, vacancy_url)
            self.set_vacancy_data(vacancy_data)

    def set_vacancy_data(self, data):
        if data['company_name']:
            company = self.set_company(data['company_name'])
        else:
            company = None

        if data['vacancy_id']:
            self.set_vacancy(data, company)

    def set_skills(self, data, vacancy):
        for skill_name in data['skills']:
            skill = Skill.objects.filter(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name)
                skill.save()
            vacancy.skills.add(skill)

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
            self.set_skills(vacancy_data, vacancy)

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

    def scrap(self, language):
        # options = Options()
        # options.headless = True
        # driver = webdriver.Firefox(options=options)
        driver = webdriver.Firefox()
        self.driver = driver
        driver.get("https://spb.hh.ru/search/vacancy?text=" + language)
        self.get_vacancies()
        driver.close()


class AreaScrapper:
    def scrap_areas(self):
        driver = webdriver.Firefox()
        self.driver = driver
        driver.get("https://spb.hh.ru/search/vacancy/advanced")
        self.driver.find_element(By.CSS_SELECTOR, '.Bloko-CompositeSelection-TreeSelectorPopup').click()
        county_rows = self.get_country_rows()
        for country_row in county_rows:
            country_data = self.get_country_data(country_row)
            self.set_country(country_data)
            country_row.find_element_by_css_selector('.bloko-modal .bloko-tree-selector-item-spacer').click()
            region_rows = self.get_region_rows(country_row)
            print(region_rows)
            return False

    def get_country_rows(self):
        return self.driver.find_elements(By.CSS_SELECTOR,
                                         '.bloko-modal .Bloko-TreeSelector-Element.bloko-tree-selector-item')

    def get_region_rows(self, country_row):
        return country_row.find_elements(By.CSS_SELECTOR,
                                         '.bloko-tree-selector-item_has-parent')

    def get_country_data(self, country_row):
        return {
            "country_area_id": country_row.find_element_by_css_selector('.bloko-checkbox__input').get_attribute(
                'value'),
            "country_name": country_row.find_element_by_css_selector('.bloko-checkbox__text').text
        }
    def set_country(self, country_data):
        country = Country.objects.filter(area_id=country_data['country_area_id']).first()
        if not country:
            country = Country(area_id=country_data['country_area_id'], name=country_data['country_name'])
            country.save()

if __name__ == '__main__':
    hh_parser = HhParser()
    hh_parser.scrap('python')
