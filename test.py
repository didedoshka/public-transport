from selenium import webdriver
from selenium.webdriver.common.by import By

class YandexMapsInterface:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.yandex.ru/maps')

        self.driver.find_element(By.CLASS_NAME, 'route-control').click() # enter routes mode

        route_panel = self.driver.find_element(By.CLASS_NAME, 'route-panel-form-view__content')

        route_panel.find_element(By.CLASS_NAME, '_mode_masstransit').click() # select public transport

        inputs_in_route_panel = route_panel.find_elements(By.TAG_NAME, 'input')
        self.route_from = inputs_in_route_panel[0]
        self.route_to = inputs_in_route_panel[1]


