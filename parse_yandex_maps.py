import YandexMapsInterface
import csv
import pickle
import sys

folder_name = f'data/{sys.argv[1]}'
with open(f'{folder_name}/data.pickle', 'rb') as file_for_data:
    data = pickle.load(file_for_data)
    print('data loaded')

ymi = YandexMapsInterface.YandexMapsInterface()

destinations = ['Покровский бульвар, 11с10', 'улица Усачёва, 6']
result = {elem['Адрес']: {'Адрес':  elem['Адрес'], 'Ссылка': elem['link']} for elem in data}
addresses = result.keys()

YandexMapsInterface.from_every_address_to_every_destination(ymi, addresses, destinations, result, folder_name)
with open(f'{folder_name}/result.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(list(result.values())[0].keys()))

    writer.writeheader()
    writer.writerows(result.values())
