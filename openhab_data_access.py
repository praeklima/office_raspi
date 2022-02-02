import requests
import sys
import pandas
import time
from datetime import datetime

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"


def openhab_read_data(openhab_url, item_name):
    try:
        url = openhab_url + item_name + "/state"  # accessing data from items
        res = requests.get(url)
        value = res.text
        if value[0] == "<":
            value = 15
        # print(value)
        #return value
    except requests.exceptions.ConnectionError:
        now = datetime.now()
        print("HTTP Openhab server exception occered", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
        value = 20
    return value


def openhab_read_list_data(openhab_url, items_list):
    output_data = []
    for i in range(0, len(items_list)):
        url = openhab_url + items_list[i] + "/state"  # accessing data from items
        try: 
            res = requests.get(url)
            value = res.text
        except requests.exceptions.ConnectionError:
            now = datetime.now()
            print("HTTP Openhab server exception occered", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
            value = 20
        output_data.append(value[0:4])
    #print(output_data)
    return output_data


def openhab_send_command(openhab_url, item_name, payload):
    url = openhab_url + item_name  # URL to publish or to send command to Wall-Plug  with payload ON
    command = payload
    #print(payload)
    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
    try:
        status = requests.post(url, headers=headers, data=command)
        status_str = str(status)
        if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
            print(item_name + ": Error status is " + str(status_str))
            return 1
        else:
            #print("Command sent successfully")
            return 0
    except requests.exceptions.ConnectionError:
        now = datetime.now()
        print("HTTP Openhab server exception occered", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
        return 0    


def openhab_send_list_commands(openhab_url, items_list, payload_list):
    #     print(items_list)
    for i in range(0, len(items_list)):
        #         print(i)
        url = openhab_url + items_list[i]  # URL to publish or to send command to Wall-Plug  with payload ON
        command = payload_list[i]
        # print(payload)
        headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
        status = requests.post(url, headers=headers, data=command)
        #         print(url + command)
        status_str = str(status)
        if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
            print(items_list[i] + ": Error status is " + str(status_str))

        #else:
            #print("Command sent successfully")

#while 1:
#    control_Algorithm = openhab_read_data(localhost_url, 'Control_Algorithm')
#    sys.stdout.write("\r")
#    print("control_Algorithm:", control_Algorithm, end='', flush=True)
#    time.sleep(5)
    