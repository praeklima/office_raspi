import openhab_data_access
import time
import sys

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"
count = 0

Tout = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Temperature_1'))
vt14 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Enocean_Temperature_1'))
vt22 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'AIR_Quality_Sensor_Temperature_2'))
vt21 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Temperature_1'))
vt40 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Temperature_3'))
Tout = round((vt14 + vt22 + vt21 + vt40) / 4, 2)

vt12 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_sensor_temperature_1'))
vt13 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Brightness_Sensor_Temperature_2'))
vt20 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'AirQualitySensor_SensorTemperature'))
vt25 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Temperature_25'))
vt26 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Temperature_26'))
vt24 = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Temperature_2'))
Tin = round((vt12 + vt13 + vt20 + vt25 + vt26 + vt24) / 6, 2)

Tcold = 18
Toptimal = 24.5
Tdew = float(openhab_data_access.openhab_read_data(cloud_api_url, 'Weather_Station_Dew_Point_1'))
Tlimit = 17

while 1:
    CO2_level = int(openhab_data_access.openhab_read_data(cloud_api_url, 'AirQualitySensor_SensorCO2'))
    # CO2 control based on the CO2 concentration reading
    if count == 0:
        # print('CO2 is ON')
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_3', 'ON')
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_4', 'ON')
    elif count == 2:
        # print('CO2 is OFF')
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_3', 'OFF')
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_4', 'OFF')
    time.sleep(30)
    count = count + 1
    sys.stdout.write("\r")
    print(count, end='', flush=True)
    if count == 6:
        count = 0
    if Tin > 21:
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_2', 'OFF')
    elif Tin < 18:
        openhab_data_access.openhab_send_command(cloud_api_url, 'Socket_Switch_2', 'ON')

    # Temperature incuded with the help of Window opening
    # T outside < T inside and T inside > 21 °C -> open window
    # T outside < T inside and T inside < 19 °C -> close window
    if Tout < Tin and Tin > 21:
        openhab_data_access.openhab_send_command(cloud_api_url, 'Window_opening_angle', '0')
    elif Tout < Tin < 19:
        openhab_data_access.openhab_send_command(cloud_api_url, 'Window_opening_angle', '99')
