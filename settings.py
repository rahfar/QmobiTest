import logging

# logging config
stream_handler = logging.StreamHandler()
stream_handler.setLevel('DEBUG')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# server config
PORT_NUMBER = 8080
relative_path_to_file = './data/ExchangeRates.xml'

# third party api
API_URL = 'www.cbr-xml-daily.ru'
API_PATH = '/daily_utf8.xml'
