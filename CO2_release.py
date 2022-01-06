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
    if 700 <= int(current_time) <= 1800:
        openhab_data_access.openhab_send_command(localhost_url,'Socket_Switch_3', 'ON')
        no_of_users = int(float(openhab_data_access.openhab_read_data(localhost_url, 'User_Intervention_CO2')))
        #print(no_of_users, '\n')
        if no_of_users == 0:
            no_of_users = 0.5
        #print(no_of_users)
        openhab_data_access.openhab_send_command(localhost_url,'Socket_Switch_4', 'ON')
        sys.stdout.write("\r")
        print("release time of CO2 and Humidifier is ", 5 * no_of_users, "seconds", end='', flush=True)
        time.sleep(5 * no_of_users)
        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_4', 'OFF')
        #print("CO2 valve 2 is OFF")
        openhab_data_access.openhab_send_command(localhost_url,'Socket_Switch_1', 'ON')
        #sys.stdout.write("\r")
        #print("release time of CO2 is ", 5 * no_of_users, "seconds", end='', flush=True)
        time.sleep(20 * no_of_users)
        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_1', 'OFF')
        time.sleep(500 - 25 * no_of_users)
    else:
        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_3', 'OFF')
        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_4', 'OFF')