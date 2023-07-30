from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class State:
    def __init__(self):
        self.text = ''

    def did_change(self, text):
        if text != self.text:
            self.text = text
            return True
        return False


class YandexMapsInterface:
    ENTER = '\uE006'

    @staticmethod
    def find_element(where, params):
        return WebDriverWait(where, timeout=3).until(EC.presence_of_element_located(params))

    @staticmethod
    def find_elements(where, params):
        return WebDriverWait(where, timeout=3).until(EC.presence_of_all_elements_located(params))

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=3)
        self.driver.get('https://www.yandex.ru/maps')

        self.find_element(self.driver, (By.CLASS_NAME, 'route-control')).click()  # enter routes mode

        route_panel = self.find_element(self.driver, (By.CLASS_NAME, 'route-panel-form-view__content'))
        self.find_element(route_panel, (By.CLASS_NAME, '_mode_masstransit')).click()  # select public transport

        inputs_in_route_panel = self.find_elements(route_panel, (By.TAG_NAME, 'input'))
        self.route_from = inputs_in_route_panel[0]
        self.route_to = inputs_in_route_panel[1]

    def set_route_from(self, street_name_from):
        self.route_from.send_keys(street_name_from + self.ENTER)


ymi = YandexMapsInterface()

ymi.set_route_from('Покровский бульвар, 11с10')

input()
