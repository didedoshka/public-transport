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
    TIME_OF_DEPARTURE = '1000'

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
            if text[1] == 'ч':
                return int(text[0]) * 60
            return int(text[0])

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.yandex.ru/maps')

        self.find_element(self.driver, (By.CLASS_NAME, 'route-control')).click()  # enter routes mode

        self.route_panel = None
        self.find_route_panel()

        self.find_element(self.route_panel, (By.CLASS_NAME, '_mode_masstransit')).click()  # select public transport

        self.duration_state = State()
        self.route_from = None
        self.route_to = None
        self.find_from_and_to_inputs()

        self.is_time_set = False

    def find_route_panel(self):
        self.route_panel = self.find_element(self.driver, (By.CLASS_NAME, 'route-panel-form-view__content'))

    def find_from_and_to_inputs(self):
        self.find_route_panel()
        inputs_in_route_panel = self.find_elements(self.route_panel, (By.TAG_NAME, 'input'))
        self.route_from = inputs_in_route_panel[0]
        self.route_to = inputs_in_route_panel[1]

    def set_time(self):
        if self.is_time_set:
            return
        self.find_route_panel()
        self.settings_element = self.find_element(self.route_panel, (By.CLASS_NAME, 'route-list-view__settings'))
        self.settings_element.click()
        self.find_route_panel()
        self.input_for_time = self.find_element(self.route_panel, (By.CSS_SELECTOR, '[placeholder="00:00"]'))
        self.input_for_time.send_keys(Keys.COMMAND, "a")
        self.input_for_time.send_keys(Keys.DELETE)
        self.input_for_time.send_keys(self.TIME_OF_DEPARTURE + Keys.ENTER)
        self.is_time_set = True

    def set_route_from(self, street_name_from):
        self.find_from_and_to_inputs()
        self.route_from.send_keys(Keys.COMMAND, "a")
        self.route_from.send_keys(Keys.DELETE)
        self.route_from.send_keys(street_name_from + Keys.ENTER)

    def set_route_to(self, street_name_to):
        self.find_from_and_to_inputs()
        self.route_to.send_keys(Keys.COMMAND, "a")
        self.route_to.send_keys(Keys.DELETE)
        self.route_to.send_keys(street_name_to + Keys.ENTER)

    def get_duration(self):
        tries = 5
        while tries > 0:
            try:
                self.find_route_panel()
                WebDriverWait(self.route_panel, timeout=2).until(lambda where: self.duration_state.did_change(
                where.find_element(By.CLASS_NAME, 'route-snippet-view').get_attribute('innerHTML')))
                break
            except:
                print(f'retrying... Tries left: {tries}')
                tries -= 1

        if tries == 0:
            raise Exception("Couldn't find duration even after 5 retries")
        duration_element = self.find_element(
            self.route_panel, (By.CLASS_NAME, 'masstransit-route-snippet-view__route-duration'))

        return self.minutes_from_text(duration_element.text)


def from_every_address_to_a_given(ymi, given_address, addresses, result, screenshot_destination=None):
    ymi.set_route_to(given_address)
    for address in addresses:
        ymi.set_route_from(address)
        ymi.set_time()
        result[address][given_address] = ymi.get_duration()
        if screenshot_destination is not None:
            ymi.driver.save_screenshot(f'{screenshot_destination}/{address} {given_address}.png')


def from_every_address_to_every_destination(ymi, addresses, destinations, result, screenshot_destination=None):
    for destination in destinations:
        from_every_address_to_a_given(ymi, destination, addresses, result, screenshot_destination)
