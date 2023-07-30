from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.implicitly_wait(5)

driver.get('https://www.yandex.ru/maps')

button = driver.find_element(By.CLASS_NAME, 'route-control')
button.click()


route_panel = driver.find_element(By.CLASS_NAME, 'route-panel-form-view__content')

public_transport_selector = route_panel.find_element(By.CLASS_NAME, '_mode_masstransit')
public_transport_selector.click()

inputs_in_route_panel = route_panel.find_elements(By.TAG_NAME, 'input')
route_from = inputs_in_route_panel[0]
route_to = inputs_in_route_panel[1]

route_from.send_keys('Покровский бульвар 11с10\uE006')
route_to.send_keys('Кременчугская 11\uE006')

duration = route_panel.find_element(By.CLASS_NAME, 'masstransit-route-snippet-view__route-duration').text

print(duration)
print(list(duration))


route_to.clear()
route_to.send_keys('Кременчугская 46\uE006')

time.sleep(3)

duration = route_panel.find_element(By.CLASS_NAME, 'masstransit-route-snippet-view__route-duration').text

print(duration)
print(list(duration))


input()
