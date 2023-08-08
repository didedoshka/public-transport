import cianparser
import datetime
import pickle
import os
import sys

folder_name = f'data/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
os.mkdir(folder_name)

data = []
data = cianparser.parse_by_url(
    deal_type="rent_long",
    accommodation_type="flat",
    location="Москва",
    search_url='https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice=42500&minprice=38000&offer_type=flat&region=1&room1=1&type=4',
    start_page=1,
    end_page=int(sys.argv[1]),
    is_saving_csv=True,
    is_express_mode=True
)
with open(f'{folder_name}/data.pickle', 'wb') as file_for_data:
    pickle.dump(data, file_for_data)
    print('data saved')
