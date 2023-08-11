import YandexMapsInterface
import csv
import pickle
import sys
from tqdm import tqdm

folder_name = f'data/{sys.argv[1]}'
with open(f'{folder_name}/data.pickle', 'rb') as file_for_data:
    data = pickle.load(file_for_data)
    print('data loaded')



def from_every_address_to_a_given(ymi, given_address, addresses, result):
    ymi.set_route_to(given_address)
    for i in tqdm(range(len(addresses))):
        address = addresses[i]
        ymi.set_route_from(address)
        ymi.set_time()
        result[i][given_address] = ymi.get_duration()

def from_every_address_to_every_destination(ymi, addresses, destinations, result):
    from_every_address_to_a_given(ymi, destinations[0], addresses, result)
    result2 = list(filter(lambda x: x[destinations[0]] <= 55, result))
    addresses2 = [elem['Адрес'] for elem in result2]
    from_every_address_to_a_given(ymi, destinations[1], addresses2, result2)
    return result2

ymi = YandexMapsInterface.YandexMapsInterface(headless=False)

destinations = ['Покровский бульвар, 11с10', 'улица Усачёва, 6']
result = [{'Адрес':  elem['address'], 'Ссылка': elem['link']} for elem in data]

addresses = [elem['Адрес'] for elem in result]

result = from_every_address_to_every_destination(ymi, addresses, destinations, result)
with open(f'{folder_name}/result.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(result[0].keys()))

    writer.writeheader()
    writer.writerows(result)
