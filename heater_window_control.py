import openhab_data_access
import time
import sys
from datetime import datetime

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"
count = 0

while 1:
    try:
        now = datetime.now()
        current_time = now.strftime("%M")
        vt12 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_sensor_temperature_1'))
    #vt13 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_Sensor_Temperature_2'))
        vt20 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'AirQualitySensor_SensorTemperature'))
        vt25 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Temperature_25'))
        vt27 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Temperature_27'))
        vt24 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Temperature_2'))
        Tin = round((vt12 + vt20 + vt25 + vt27 + vt24) / 5, 2)
        now = datetime.now()
        sys.stdout.write("\r")
        print(now.strftime("%Y-%m-%d %H:%M:%S"),": Tin = ", Tin,"; Heater is ",openhab_data_access.openhab_read_data(localhost_url, 'Socket_Switch_2'), end='', flush=True)
        openhab_data_access.openhab_send_command(localhost_url,'Inside_temperature', str(Tin))
    
        #if Tin > 22:
        #    openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'OFF')
        #elif Tin < 20.5:
        #    openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'ON')
        #time.sleep(5)
        if Tin > 22:
            openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'OFF')
        
        elif int(current_time) <= 20:
            openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'ON')
        else:
            openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'OFF')
        time.sleep(5)
        lux_outside = float(openhab_data_access.openhab_read_data(localhost_url, 'Multisensor_outside_SensorLuminance'))
        if lux_outside < 1000:
            openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_51', 'ON')
        else:
            openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_51', 'OFF')
            
    #if Tin < 18:
    #    openhab_data_access.openhab_send_data(localhost_url, 'Socket_Switch_2', 'ON')
    #    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '0')
    #time.sleep(10)
#elif Tin >15:
#    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '99')
#    openhab_data_access.openhab_send_data(localhost_url, 'Socket_Switch_1', 'OFF')
    except ValueError:
        print("Value Error due to HTTP Openhab server exception occered", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))
        
    