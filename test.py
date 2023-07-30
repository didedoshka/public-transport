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
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=3)
        self.driver.get('https://www.yandex.ru/maps')

        elem = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'route-control'))) # enter routes mode
        elem.click()
        # self.wait.find_element(By.CLASS_NAME, 'route-control').click() # enter routes mode

        # route_panel = self.driver.find_element(By.CLASS_NAME, 'route-panel-form-view__content')
        #
        # route_panel.find_element(By.CLASS_NAME, '_mode_masstransit').click() # select public transport
        #
        # inputs_in_route_panel = route_panel.find_elements(By.TAG_NAME, 'input')
        # self.route_from = inputs_in_route_panel[0]
        # self.route_to = inputs_in_route_panel[1]
        #


ymi = YandexMapsInterface()

input()
