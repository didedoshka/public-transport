import yandex_realty_parser
import datetime
import pickle
import os
import sys

folder_name = f'data/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
os.mkdir(folder_name)

end_page = None
if len(sys.argv) > 1:
    end_page = int(sys.argv[1])
data = yandex_realty_parser.parse(
    'https://realty.ya.ru/moskva/snyat/kvartira/odnokomnatnaya/?commuteTransport=PUBLIC&commuteTime=45&commutePointLatitude=55.75345&commutePointLongitude=37.64823&commuteAddress=%D0%9F%D0%BE%D0%BA%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B1%D1%83%D0%BB%D1%8C%D0%B2%D0%B0%D1%80%2C%2011%D1%8110&priceMin=38500&priceMax=42500', end_page=end_page)


with open(f'{folder_name}/data.pickle', 'wb') as file_for_data:
    pickle.dump(data, file_for_data)
    print('data saved')
