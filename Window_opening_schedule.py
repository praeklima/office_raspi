# import paho.mqtt.client as mqtt
import requests
import time
from datetime import datetime
import openhab_data_access
import sys

cloud_api_url = "https://praeklima.tud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"
count = 0

while True:
    now = datetime.now()
    current_time = now.strftime("%H%M")
    #count = count +1
    #print(count)
    current_position = int(openhab_data_access.openhab_read_data(localhost_url, 'Window_opening_angle'))
    if int(current_time) == 900 or int(current_time) == 1200 or int(current_time) == 1500:
        com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '99')
        time.sleep(300)
    else:
        if current_position != 0:
            com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '0')
        
    