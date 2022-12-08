import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from fake_useragent import UserAgent
from datetime import date

lst = ['name', 'description', 'employer', 'link']
with open(f'{date.today()}.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(lst)

class VacanciesBot():

    def __init__(self):

       self.browser = webdriver.Chrome()

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def search_tproger(self):

        # Searching vacansies on tproger.ru

        url = 'https://tproger.ru/jobs/?skill=python'

        useragent = UserAgent()

        options = webdriver.ChromeOptions()
        # options.add_argument("--proxy-server=5.45.64.97:3128")
        # options.add_argument(f'user-agent={useragent.ie}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        browser = webdriver.Chrome(options=options)

        try:
            browser.get(url=url)
            print('Searching in Tproger')
            time.sleep(3)

            for i in range(0, 2):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 5))

            vacancies = browser.find_elements(By.CLASS_NAME, 'vacancy-card')
            for vacancy in vacancies:
                blank = vacancy.find_element(By.TAG_NAME, 'a').get_attribute('href')
                time.sleep(1)
                browser.execute_script(f'window.open("{blank}");')
                time.sleep(random.randrange(1, 3))
                browser.switch_to.window(browser.window_handles[1])
                time.sleep(1)
                name = browser.find_element(By.TAG_NAME, 'h1').text.strip()
                description = browser.find_element(By.CLASS_NAME, 'single__content').text
                employer = browser.find_element(By.XPATH, '//a[@class="widget-caption-a hoverable"]').text
                info = [name, description, employer, blank]

                with open(f'{date.today()}.csv', 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(info)
                print(f'vacancy {blank} was written')

                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(3)

            self.close_browser()

        except Exception as ex:
            print(ex)
            print('Tproger failed me!')
            self.close_browser()

    def search_geekjob(self):

        # Searching vacansies on geekjob.ru

        url = 'https://geekjob.ru/vacancies?qs=python'

        useragent = UserAgent()

        options = webdriver.ChromeOptions()
        # options.add_argument("--proxy-server=5.45.64.97:3128")
        # options.add_argument(f'user-agent={useragent.ie}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        browser = webdriver.Chrome(options=options)

        try:
            browser.get(url=url)
            print('Searching in Geekjob')
            time.sleep(3)

            for i in range(0, 2):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 5))

                vacancies = browser.find_elements(By.XPATH, '//a[@class="title"]')

                for vacancy in vacancies:
                    blank = vacancy.get_attribute('href')
                    time.sleep(1)
                    browser.execute_script(f'window.open("{blank}");')
                    time.sleep(random.randrange(1, 3))
                    browser.switch_to.window(browser.window_handles[1])
                    time.sleep(1)
                    name = browser.find_element(By.TAG_NAME, 'h1').text.strip()
                    description = browser.find_element(By.ID, 'vacancy-description').text
                    employer = browser.find_element(By.TAG_NAME, 'h5').text.strip()
                    info = [name, description, employer, blank]

                    with open(f'{date.today()}.csv', 'a', newline='', encoding='utf-8-sig') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(info)

                    print(f'vacancy {blank} was written')
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                    time.sleep(3)

            self.close_browser()

        except Exception as ex:
            print(ex)
            print('Geekjob failed me!')
            self.close_browser()

    def search_habr(self):

        # Genuine headache

        useragent = UserAgent()

        options = webdriver.ChromeOptions()
        # options.add_argument("--proxy-server=5.45.64.97:3128")
        # options.add_argument(f'user-agent={useragent.ie}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        browser = webdriver.Chrome(options=options)

        try:
            print('Searching in Habr')
            for i in range(1, 3):
                browser.get(url=f'https://career.habr.com/vacancies?page={i}&skills[]=446&type=all')
                time.sleep(3)

                vacancies = browser.find_elements(By.XPATH, '//a[@class="vacancy-card__title-link"]')
                for vacancy in vacancies:
                    blank = vacancy.get_attribute('href')
                    time.sleep(1)
                    browser.execute_script(f'window.open("{blank}");')
                    time.sleep(random.randrange(1, 3))
                    browser.switch_to.window(browser.window_handles[1])
                    time.sleep(1)
                    name = browser.find_element(By.TAG_NAME, 'h1').text.strip()
                    if name == 'Ошибка 404':
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        time.sleep(3)

                    else:
                        description = browser.find_element(By.CLASS_NAME, 'vacancy-description__text').text
                        employer = [x.text for x in browser.find_elements(By.TAG_NAME, 'div')]
                        time.sleep(1)
                        info = [name, description, employer[64], blank]

                        with open(f'{date.today()}.csv', 'a', newline='', encoding='utf-8-sig') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow(info)
                        print(f'vacancy {blank} was written')
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        time.sleep(3)

                self.close_browser()

        except Exception as ex:
            print(ex)
            print('Goddamn Habr!')
            self.close_browser()

    def main(self):
        VacanciesBot().search_tproger()
        VacanciesBot().search_geekjob()
        VacanciesBot().search_habr()

if __name__ == '__main__':
    my_bot = VacanciesBot()
    my_bot.main()

