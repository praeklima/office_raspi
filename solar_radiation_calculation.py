import requests
from datetime import datetime
import time

print('Solar Radiation Calculation')
cloud_api_url = "https://praeklima.tud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"

column = ['Luminance_Sensor_Luminance_1', 'Luminance_Sensor_Luminance_2', 'Solar_radiation_1', 'Solar_radiation_2']
while True:
    for i in range(0, 2):
        url = localhost_url + column[i] + "/state"  # accessing data from items
        res = requests.get(url)
        value = res.text
        #print(value)
        url = localhost_url + column[i+2]
        headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
        payload = str(round(int(value) * 0.0079,2))
        #print(payload)
        status = requests.post(url, headers=headers, data=payload)
        # print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
        status_str = str(status)
    time.sleep(10)