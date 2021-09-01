import requests 
import pandas
import sys
import time
import mysql.connector
from datetime import datetime



Sleep_time = 29  # Frequency of data to be collected in seconds
No_of_Data_samples = 30   # No of data samples required with a frequency of Sleep_time
database = pandas.read_csv('~/Praeklima/REST_API_database', low_memory=False)  # Opening csv file using pandas

print("working")

#openhab cloud REST API URL syntax https://<user_emailid>:<password>@home.myopenhab.org/rest/items 
cloud_api_url = "https://praeklima.tud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/" #Use cloud url to grab data from other network
localhost_url = "http://localhost:8080/rest/items/"
# Column names for the database
column = ['date', 'time', 'localCurrentTemperature', 'localCurrentApparentTemperature', 'LocalForecastedTemperature_3',
          'LocalForecastedApparentTemperature_3', 'LocalForecastedTemperature_6',
          'LocalForecastedApparentTemperature_6', 'localCurrentHumidity', 'LocalForecastedHumidity_3',
          'LocalForecastedHumidity_6', 'LocalCurrent_Cloudiness', 'LocalForecastedCloudiness_3',
          'LocalForecastedCloudiness_6', 'localCurrentUVIndex', 'LocalCurrent_Rain', 'LocalForecastedRain_3',
          'LocalForecastedRain_6',
          'LocalCurrent_Snow', 'LocalForecastedSnow_3', 'LocalForecastedSnow_6', 'SensorTemperature',
          'SensorRelativeHumidity', 'SensorUltraviolet', 'SensorLuminance', 'MotionAlarm', 'TamperAlarm',
          'WallPlugSwitch1_Switch_1', 'WallPlugSwitch1_SensorPower_1','Multisensor_outside_SensorTemperature',
          'Multisensor_outside_SensorRelativeHumidity', 'Multisensor_outside_SensorUltraviolet', 'Multisensor_outside_SensorLuminance',
          'Multisensor_outside_TamperAlarm', 'Multisensor_outside_MotionAlarm',
          'sensor1_temperature', 'sensor2_temperature', 'sensor3_temperature',
                      'sensor4_temperature', 'sensor5_temperature',
                      'sensor1_humidity', 'sensor2_humidity', 'sensor3_humidity', 'sensor4_humidity',
                      'sensor5_humidity',
                      'Enocean_Temperature_1', 'Enocean_Humidity_1', 'Brightness_sensor_temperature_1',
                      'Brightness_Sensor_Temperature_2',
                      'Brightness_Sensor_Ambient_Brightness_1', 'Brightness_Sensor_Ambient_Brightness_2',
                      'Brightness_Sensor_Motion_detection_1',
                      'Brightness_Sensor_Motion_detection_2', 'Brightness_Sensor_Battery_1',
                      'Brightness_Sensor_Battery_2',
                      'Socket_Energy_1', 'Socket_Energy_2', 'Socket_Power_1', 'Socket_Power_2', 'Socket_Switch_1',
                      'Socket_Switch_2', 'Socket_Energy_3', 'Socket_Energy_4', 'Socket_Power_3', 'Socket_Power_4',
                      'Socket_Switch_3', 'Socket_Switch_4',
                      'Luminance_Sensor_Luminance_1', 'Luminance_Sensor_Luminance_2', 'Luminance_Sensor_Battery_1',
                      'Luminance_Sensor_Battery_2',
                      'Rain_Sensor_Precipitation_1', 'Rain_Sensor_Water_Meter_1', 'Rain_Sensor_Battery_1',
                      'AIR_Quality_Sensor_CO2_2',
                      'AIR_Quality_Sensor_Dew_point_2', 'AIR_Quality_Sensor_Humidity_2',
                      'AIR_Quality_Sensor_Temperature_2',
                      'AIR_Quality_Sensor_VOC_2',
                      'AirQualitySensor_SensorTemperature',
                      'AirQualitySensor_SensorRelativeHumidity', 'AirQualitySensor_SensorVOLATILE_ORGANIC_COMPOUND',
                      'AirQualitySensor_SensorDewPoint', 'AirQualitySensor_SensorCO2',
                      'Weather_Station_Air_Pressure_1', 'Weather_Station_Dew_Point_1',
                      'Weather_Station_Electricity_meter_1',
                      'Weather_Station_Heat_meter_1', 'Weather_Station_Humidity_1', 'Weather_Station_Luminance_1',
                      'Weather_Station_Temperature_1', 'Weather_Station_Wind_Speed_1','Weather_Station_Air_Pressure_2', 'Weather_Station_Dew_Point_2',
                      'Weather_Station_Electricity_meter_2',
                      'Weather_Station_Heat_meter_2', 'Weather_Station_Humidity_2', 'Weather_Station_Luminance_2',
                      'Weather_Station_Temperature_2', 'Weather_Station_Wind_Speed_2',
                      'Rain_Sensor_Precipitation_2', 'Rain_Sensor_Water_Meter_2', 'Rain_Sensor_Battery_2',
                      'Temperature_25', 'Temperature_26', 'Temperature_27', 'wind_sensor_power', 'wind_sensor_energy']

openhab_items = "(date,time,localCurrentTemperature,localCurrentApparentTemperature,LocalForecastedTemperature_3,LocalForecastedApparentTemperature_3,LocalForecastedTemperature_6,LocalForecastedApparentTemperature_6,localCurrentHumidity,LocalForecastedHumidity_3,LocalForecastedHumidity_6,LocalCurrent_Cloudiness,LocalForecastedCloudiness_3,LocalForecastedCloudiness_6,localCurrentUVIndex,LocalCurrent_Rain,LocalForecastedRain_3,LocalForecastedRain_6,LocalCurrent_Snow,LocalForecastedSnow_3,LocalForecastedSnow_6,SensorTemperature,SensorRelativeHumidity,SensorUltraviolet,SensorLuminance,MotionAlarm,TamperAlarm,WallPlugSwitch1_Switch_1,WallPlugSwitch1_SensorPower_1,Multisensor_outside_SensorTemperature,Multisensor_outside_SensorRelativeHumidity,Multisensor_outside_SensorUltraviolet,Multisensor_outside_SensorLuminance,Multisensor_outside_TamperAlarm,Multisensor_outside_MotionAlarm,sensor1_temperature,sensor2_temperature,sensor3_temperature,sensor4_temperature,sensor5_temperature,sensor1_humidity,sensor2_humidity,sensor3_humidity,sensor4_humidity,sensor5_humidity,Enocean_Temperature_1,Enocean_Humidity_1,Brightness_sensor_temperature_1,Brightness_Sensor_Temperature_2,Brightness_Sensor_Ambient_Brightness_1,Brightness_Sensor_Ambient_Brightness_2,Brightness_Sensor_Motion_detection_1,Brightness_Sensor_Motion_detection_2,Brightness_Sensor_Battery_1,Brightness_Sensor_Battery_2,Socket_Energy_1,Socket_Energy_2,Socket_Power_1,Socket_Power_2,Socket_Switch_1,Socket_Switch_2,Socket_Energy_3,Socket_Energy_4,Socket_Power_3,Socket_Power_4,Socket_Switch_3,Socket_Switch_4,Luminance_Sensor_Luminance_1,Luminance_Sensor_Luminance_2,Luminance_Sensor_Battery_1,Luminance_Sensor_Battery_2,Rain_Sensor_Precipitation_1,Rain_Sensor_Water_Meter_1,Rain_Sensor_Battery_1,AIR_Quality_Sensor_CO2_2,AIR_Quality_Sensor_Dew_point_2,AIR_Quality_Sensor_Humidity_2,AIR_Quality_Sensor_Temperature_2,AIR_Quality_Sensor_VOC_2,AirQualitySensor_SensorTemperature,AirQualitySensor_SensorRelativeHumidity,AirQualitySensor_SensorVOLATILE_ORGANIC_COMPOUND,AirQualitySensor_SensorDewPoint,AirQualitySensor_SensorCO2,Weather_Station_Air_Pressure_1,Weather_Station_Dew_Point_1,Weather_Station_Electricity_meter_1,Weather_Station_Heat_meter_1,Weather_Station_Humidity_1,Weather_Station_Luminance_1,Weather_Station_Temperature_1,Weather_Station_Wind_Speed_1, Weather_Station_Air_Pressure_2, Weather_Station_Dew_Point_2, Weather_Station_Electricity_meter_2, Weather_Station_Heat_meter_2, Weather_Station_Humidity_2, Weather_Station_Luminance_2, Weather_Station_Temperature_2, Weather_Station_Wind_Speed_2,Rain_Sensor_Precipitation_2,Rain_Sensor_Water_Meter_2,Rain_Sensor_Battery_2,Temperature_25,Temperature_26,Temperature_27,wind_sensor_power, wind_sensor_energy)"
specifier = "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

row_data = []
data = []
count = 0

mydb = mysql.connector.connect(
host="daten.praeklima.de",
user="tudresden",
password="k-Dnn1Qqw.sddFI",
database="tudresden")

while True:     # infinite loop
    now = datetime.now()
    row_data = [now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]  # time stamp for data collection
    for i in range(2, len(column)):
        url = localhost_url + column[i] + "/state"  # accessing data from items
        res = requests.get(url)
        value = res.text
        if 1 < i < 8 or i == 21 or i == 29:    # Removing units from the data
            value = value[:len(value) - 4]
        elif 14 < i < 21:
            value = value[:len(value) - 3]
        elif 7 < i < 14:
            value = value[:len(value) - 2]
        row_data.append(value)
    count = count + 1
    data.append(row_data)
    #print(row_data)
    mycursor = mydb.cursor()
    sql = "INSERT INTO openhab_items_data "+openhab_items + "VALUES " + specifier
    #print(sql)
    val = row_data
    mycursor.execute(sql, val)
    mydb.commit()
    
    time.sleep(Sleep_time)
#     print(count)
    sys.stdout.write("\r")
    print(count, end='', flush=True)
    if count == No_of_Data_samples:
        count = 0
#         print(data)
        df = pandas.DataFrame(data, columns=column)  # Creating a Pandas database for current data
#         print(df)
        database = database.append(df, ignore_index=True)  # appending new data to the main REST_API_database
#         print(database)
        database.to_csv('REST_API_database', index=False)  # Converting it into csv file
        data = []
