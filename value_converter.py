import xml.etree.ElementTree as ET
import os
import http.client
import time
import logging
import settings

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(settings.stream_handler)


def download_exchange_rates(file_path: str) -> None:
    logger.info('making request')
    conn = http.client.HTTPSConnection(settings.API_URL)
    conn.request('GET', settings.API_PATH)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    with open(file_path, 'w') as f:
        f.write(data)


def convert_usd_to_rub(value: float) -> (float, float):
    file_path = os.path.join(os.path.dirname(__file__), settings.relative_path_to_file)
    if os.path.exists(file_path) and (time.time() - os.path.getctime(file_path) < 60 * 60 * 24):
        root = ET.parse(file_path).getroot()
    else:
        logger.info('file does not exists or too old')
        download_exchange_rates(file_path)
        root = ET.parse(file_path).getroot()

    for tag in root.iter():
        if tag.get('ID') == 'R01235':
            exchange_rate = float(tag.find('Value').text.replace(',', '.'))
            logger.debug(f'exchange rate {exchange_rate}')
            break

    return exchange_rate * value, exchange_rate
