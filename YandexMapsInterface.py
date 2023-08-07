from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os
import csv
import time


class State:
    def __init__(self):
        self.text = ''

    def did_change(self, text):
        if text != self.text:
            self.text = text
            return True
        return False


class YandexMapsInterface:
    TIMEOUT = 10

    @classmethod
    def find_element(cls, where, params):
        return WebDriverWait(where, timeout=cls.TIMEOUT).until(EC.presence_of_element_located(params))

    @classmethod
    def find_elements(cls, where, params):
        return WebDriverWait(where, timeout=cls.TIMEOUT).until(EC.presence_of_all_elements_located(params))

    @staticmethod
    def minutes_from_text(text):
        text = text.split()
        if len(text) == 4:
            return int(text[0]) * 60 + int(text[2])
        else:
            return int(text[0])

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=3)
        self.driver.get('https://www.yandex.ru/maps')

        self.find_element(self.driver, (By.CLASS_NAME, 'route-control')).click()  # enter routes mode

        self.route_panel = self.find_element(self.driver, (By.CLASS_NAME, 'route-panel-form-view__content'))
        self.find_element(self.route_panel, (By.CLASS_NAME, '_mode_masstransit')).click()  # select public transport

        inputs_in_route_panel = self.find_elements(self.route_panel, (By.TAG_NAME, 'input'))
        self.route_from = inputs_in_route_panel[0]
        self.route_to = inputs_in_route_panel[1]

        self.duration_state = State()

    def set_route_from(self, street_name_from):
        self.route_from.send_keys(Keys.COMMAND, "a")
        self.route_from.send_keys(Keys.DELETE)
        self.route_from.send_keys(street_name_from + Keys.ENTER)
        time.sleep(7)

    def set_route_to(self, street_name_to):
        self.route_to.send_keys(Keys.COMMAND, "a")
        self.route_to.send_keys(Keys.DELETE)
        self.route_to.send_keys(street_name_to + Keys.ENTER)

    def get_duration(self):
        WebDriverWait(self.route_panel, timeout=self.TIMEOUT).until(lambda where: self.duration_state.did_change(
            where.find_element(By.CLASS_NAME, 'route-snippet-view').get_attribute('innerHTML')))
        # print(self.duration_state.text)
        duration_element = self.find_element(
            self.route_panel, (By.CLASS_NAME, 'masstransit-route-snippet-view__route-duration'))

        return self.minutes_from_text(duration_element.text)


if __name__ == "__main__":
    folder_name = str(datetime.datetime.now().replace(microsecond=0))
    os.mkdir(folder_name)

    destinations = ['Покровский бульвар, 11с10', 'улица Усачёва, 6']

    ymi = YandexMapsInterface()

    def from_every_address_to_a_given(given_address, addresses, result):
        ymi.set_route_to(given_address)
        for address in addresses:
            ymi.set_route_from(address)
            result[address][given_address] = ymi.get_duration()
            ymi.driver.save_screenshot(f'{folder_name}/{address} {given_address}.png')

    with open('list.txt', 'r') as input_list:
        result = {}
        addresses = list(map(str.rstrip, input_list.readlines()))
        for address in addresses:
            result[address] = {}

        for destination in destinations:
            from_every_address_to_a_given(destination, addresses, result)

        output = []
        for address in addresses:
            output.append(result[address])
            output[-1]['Адрес'] = address


        with open(f'{folder_name}/result.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Адрес'] + destinations)

            writer.writeheader()
            writer.writerows(output)
