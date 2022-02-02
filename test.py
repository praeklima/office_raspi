import openhab_data_access
import time
import sys
from datetime import datetime

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"
count = 0

while 1:
    print(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_sensor_temperature_1'))
    vt12 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_sensor_temperature_1'))