import requests
from datetime import datetime

cloud_api_url = "https://praeklima.tud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"

column = ['Ventilation_Flap_switch', 'Window_blinds', 'Window_opening_angle']
for i in range(0, len(column)):
    url = localhost_url + column[i] + "/state"  # accessing data from items
    res = requests.get(url)
    value = res.text
    print(value)
value = '{"value": "'+ value+ '"}'
print(value)

now = datetime.now()
print(now)