import paho.mqtt.client as mqtt
import requests
import time
import sys
from datetime import datetime

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"

# Dictonary of MQTT Feeds/topics, add the topics of the broker in this Dictonary
column = ['casenio/event/f8f005d87424/7/1/JSON', 'casenio/event/f8f005d87424/8/1/JSON',
          'casenio/event/f8f005d87424/9/1/JSON', 'casenio/event/f8f005d87424/10/1/JSON',
          'casenio/event/f8f005d87424/11/1/JSON', 'casenio/event/f8f005d87424/7/5/JSON',
          'casenio/event/f8f005d87424/8/5/JSON', 'casenio/event/f8f005d87424/9/5/JSON',
          'casenio/event/f8f005d87424/10/5/JSON', 'casenio/event/f8f005d87424/11/5/JSON',
          'casenio/event/f8f005d87424/14/1/JSON', 'casenio/event/f8f005d87424/14/5/JSON',
          'casenio/event/f8f005d87424/12/1/JSON', 'casenio/event/f8f005d87424/13/1/JSON',
          'casenio/event/f8f005d87424/12/3/JSON', 'casenio/event/f8f005d87424/13/3/JSON',
          'casenio/event/f8f005d87424/12/305/JSON', 'casenio/event/f8f005d87424/13/305/JSON',
          'casenio/event/f8f005d87424/12/602/JSON', 'casenio/event/f8f005d87424/13/602/JSON',
          'casenio/event/f8f005d87424/15/200/JSON', 'casenio/event/f8f005d87424/16/200/JSON',
          'casenio/event/f8f005d87424/15/4/JSON', 'casenio/event/f8f005d87424/16/4/JSON',
          'casenio/event/f8f005d87424/15/302/JSON', 'casenio/event/f8f005d87424/16/302/JSON',
          'casenio/event/f8f005d87424/35/200/JSON', 'casenio/event/f8f005d87424/36/200/JSON',
          'casenio/event/f8f005d87424/35/4/JSON', 'casenio/event/f8f005d87424/36/4/JSON',
          'casenio/event/f8f005d87424/35/302/JSON', 'casenio/event/f8f005d87424/36/302/JSON',
          'casenio/event/f8f005d87424/58/69/JSON', 'casenio/event/f8f005d87424/18/69/JSON',
          'casenio/event/f8f005d87424/58/602/JSON', 'casenio/event/f8f005d87424/18/602/JSON',
          'casenio/event/f8f005d87424/19/12/JSON', 'casenio/event/f8f005d87424/19/202/JSON',
          'casenio/event/f8f005d87424/19/602/JSON', 'casenio/event/f8f005d87424/22/17/JSON',
          'casenio/event/f8f005d87424/22/11/JSON', 'casenio/event/f8f005d87424/22/5/JSON',
          'casenio/event/f8f005d87424/22/1/JSON', 'casenio/event/f8f005d87424/22/39/JSON',
          'casenio/event/f8f005d87424/20/1/JSON', 'casenio/event/f8f005d87424/20/5/JSON',
          'casenio/event/f8f005d87424/20/39/JSON', 'casenio/event/f8f005d87424/20/11/JSON',
          'casenio/event/f8f005d87424/20/17/JSON', 'casenio/event/f8f005d87424/21/9/JSON',
          'casenio/event/f8f005d87424/21/11/JSON', 'casenio/event/f8f005d87424/21/200/JSON',
          'casenio/event/f8f005d87424/21/203/JSON', 'casenio/event/f8f005d87424/21/5/JSON',
          'casenio/event/f8f005d87424/21/3/JSON', 'casenio/event/f8f005d87424/21/1/JSON',
          'casenio/event/f8f005d87424/21/6/JSON', 'casenio/event/f8f005d87424/24/9/JSON',
          'casenio/event/f8f005d87424/24/11/JSON', 'casenio/event/f8f005d87424/24/200/JSON',
          'casenio/event/f8f005d87424/24/203/JSON', 'casenio/event/f8f005d87424/24/5/JSON',
          'casenio/event/f8f005d87424/24/3/JSON', 'casenio/event/f8f005d87424/24/1/JSON',
          'casenio/event/f8f005d87424/24/6/JSON', 'casenio/event/f8f005d87424/23/12/JSON', 
          'casenio/event/f8f005d87424/23/202/JSON', 'casenio/event/f8f005d87424/23/602/JSON',
          'casenio/event/f8f005d87424/25/1/JSON', 'casenio/event/f8f005d87424/26/1/JSON',
          'casenio/event/f8f005d87424/27/1/JSON', 
          'casenio/event/f8f005d87424/57/4/JSON', 'casenio/event/f8f005d87424/57/200/JSON',
          'casenio/event/f8f005d87424/56/4/JSON', 'casenio/event/f8f005d87424/56/200/JSON',
          'casenio/event/f8f005d87424/53/4/JSON', 'casenio/event/f8f005d87424/53/200/JSON',
          #'casenio/event/f8f005d87424/42/4/JSON', 'casenio/event/f8f005d87424/42/200/JSON',
          'casenio/event/f8f005d87424/40/9/JSON',
          'casenio/event/f8f005d87424/40/11/JSON', 'casenio/event/f8f005d87424/40/200/JSON',
          'casenio/event/f8f005d87424/40/203/JSON', 'casenio/event/f8f005d87424/40/5/JSON',
          'casenio/event/f8f005d87424/40/3/JSON', 'casenio/event/f8f005d87424/40/1/JSON',
          'casenio/event/f8f005d87424/40/6/JSON', 'casenio/event/f8f005d87424/43/17/JSON',
          'casenio/event/f8f005d87424/43/11/JSON', 'casenio/event/f8f005d87424/43/5/JSON',
          'casenio/event/f8f005d87424/43/1/JSON', 'casenio/event/f8f005d87424/43/39/JSON',
          'casenio/event/f8f005d87424/44/17/JSON',
          'casenio/event/f8f005d87424/44/11/JSON', 'casenio/event/f8f005d87424/44/5/JSON',
          'casenio/event/f8f005d87424/44/1/JSON', 'casenio/event/f8f005d87424/44/39/JSON',
          'casenio/event/f8f005d87424/45/17/JSON',
          'casenio/event/f8f005d87424/45/11/JSON', 'casenio/event/f8f005d87424/45/5/JSON',
          'casenio/event/f8f005d87424/45/1/JSON', 'casenio/event/f8f005d87424/45/39/JSON',
          'casenio/event/f8f005d87424/51/302/JSON', 'casenio/event/f8f005d87424/51/4/JSON',
          'casenio/event/f8f005d87424/51/200/JSON', 'casenio/event/f8f005d87424/60/4/JSON',
          'casenio/event/f8f005d87424/60/200/JSON', 'casenio/event/f8f005d87424/59/302/JSON',
          'casenio/event/f8f005d87424/59/4/JSON',   'casenio/event/f8f005d87424/59/200/JSON',
          'casenio/event/f8f005d87424/50/598/JSON']

# Openhab items, where the MQTT topics data is to be stored on Openhab items, "place the list in the same order as MQTT topics"
openhab_item_names = ['sensor1_temperature', 'sensor2_temperature', 'sensor3_temperature',
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
                      'Temperature_25', 'Temperature_26', 'Temperature_27', 'wind_sensor_power', 'wind_sensor_energy', 'Window_opening_power', 'Window_opening_energy',
                      'Slats_angle_power', 'Slats_angle_energy',# 'Window_blinds_power', 'Window_blinds_energy',
                      'Weather_Station_Air_Pressure_3', 'Weather_Station_Dew_Point_3',
                      'Weather_Station_Electricity_meter_3',
                      'Weather_Station_Heat_meter_3', 'Weather_Station_Humidity_3', 'Weather_Station_Luminance_3',
                      'Weather_Station_Temperature_3', 'Weather_Station_Wind_Speed_3', 'AIR_Quality_Sensor_CO2_3',
                      'AIR_Quality_Sensor_Dew_point_3', 'AIR_Quality_Sensor_Humidity_3',
                      'AIR_Quality_Sensor_Temperature_3', 'AIR_Quality_Sensor_VOC_3','AIR_Quality_Sensor_CO2_4',
                      'AIR_Quality_Sensor_Dew_point_4', 'AIR_Quality_Sensor_Humidity_4',
                      'AIR_Quality_Sensor_Temperature_4', 'AIR_Quality_Sensor_VOC_4',
                      'AIR_Quality_Sensor_CO2_5','AIR_Quality_Sensor_Dew_point_5', 'AIR_Quality_Sensor_Humidity_5', 'AIR_Quality_Sensor_Temperature_5', 'AIR_Quality_Sensor_VOC_5',
                      'Socket_Switch_51','Socket_power_51','Socket_Energy_51', 'Window_blinds_power_consumption', 'Window_blinds_energy_consumption', 'raspberrypi_switch',
                      'raspberrypi_power', 'raspberrypi_energy', 'Lunos_Ventilation_Mode']

actuators = ['Socket_Switch_51','Ventilation_Flap_switch', 'Socket_Switch_1', 'Socket_Switch_2', 'Socket_Switch_3', 'Socket_Switch_4','Brightness_Sensor_Motion_detection_1', 'Brightness_Sensor_Motion_detection_2']

timestamps_list = ['AIR_Quality_Sensor_CO2_2_time_stamp', 'AIR_Quality_Sensor_CO2_1_time_stamp', 'AIR_Quality_Sensor_CO2_3_time_stamp', 'AIR_Quality_Sensor_CO2_4_time_stamp', 'AIR_Quality_Sensor_CO2_5_time_stamp']
timestamps_items = ['AIR_Quality_Sensor_CO2_2', 'AirQualitySensor_SensorCO2', 'AIR_Quality_Sensor_CO2_3', 'AIR_Quality_Sensor_CO2_4', 'AIR_Quality_Sensor_CO2_5']
print("PAHO_MQTT")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        subscribe_mqtt()
    else:
        print("Connect returned result code: " + str(rc))


payload = 0


# The callback for when a PUBLISH message is received from the server.
# Callback Definition: subscribed topics data will be received and will commit that data to the respective openhab item
def on_message(client, userdata, msg):
    global payload
    now = datetime.now()
    sys.stdout.write("\r")
    print(now.strftime("%Y-%m-%d %H:%M:%S"), end='', flush=True)
    #print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    #print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"), end='', flush=True)
    if msg.topic =='casenio/event/f8f005d87424/58/69/JSON':# or msg.topic =='casenio/event/f8f005d87424/16/200/JSON' or msg.topic =='casenio/event/f8f005d87424/16/302/JSON':
        print(msg.payload.decode("utf-8"))
    
    if msg.topic == 'casenio/event/f8f005d87424/50/1/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print('fan 52')
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                payload = payload_received[7:j]
                break
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                if payload_received[i+6] == '0':
                    url = localhost_url + 'temperature_inside_50'
                                                        
                elif payload_received[i+6] == '1':
                    url = localhost_url + 'temperature_outside_50'
                            
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                status = requests.post(url, headers=headers, data=payload)
                #print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
                if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                    print(openhab_item_names[i] + " set to " + payload + ": " + str(status))

    if msg.topic == 'casenio/event/f8f005d87424/50/5/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print('fan 52')
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                payload = payload_received[7:j]
                break
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                if payload_received[i+6] == '0':
                    url = localhost_url + 'humidity_inside_50'
                                                        
                elif payload_received[i+6] == '1':
                    url = localhost_url + 'humidity_outside_50'
                            
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                status = requests.post(url, headers=headers, data=payload)
                #print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
                if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                    print(openhab_item_names[i] + " set to " + payload + ": " + str(status))

    if msg.topic == 'casenio/event/f8f005d87424/50/18/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print('fan 52')
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                payload = payload_received[7:j]
                break
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                if payload_received[i+6] == '0':
                    url = localhost_url + 'Supply_air_flow_50'
                                                        
                elif payload_received[i+6] == '1':
                    url = localhost_url + 'exhaust_air_flow_50'
                            
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                status = requests.post(url, headers=headers, data=payload)
                #print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
                if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                    print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    
                    
    if msg.topic == 'casenio/event/f8f005d87424/39/15/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print(payload_received)
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                payload = payload_received[7:j]
                break
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                if payload_received[i+6] == '6':
                    url = localhost_url + 'wind_sensor_channel_6'
                                                        
                elif payload_received[i+6] == '7':
                    url = localhost_url + 'wind_sensor_channel_7'
                                
                elif payload_received[i+6] == '8':
                    url = localhost_url + 'wind_sensor_channel_8'
                        
                elif payload_received[i+6] == '9':
                    url = localhost_url + 'wind_sensor_channel_9'
                        
                else:
                    url = localhost_url + 'wind_sensor_channel_0'
                            
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                status = requests.post(url, headers=headers, data=payload)
                #print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
                if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                    print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                                # print("Error status is " + str(status_str))
                                
    if msg.topic == 'casenio/event/f8f005d87424/49/15/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print(payload_received)
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                temp = payload_received[7:j]
                
                break
        payload = str(format((float(temp)*9) - 20, '.2f'))    
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                if payload_received[i+6] == '3':
                    url = localhost_url + 'Temperature_sensor_outside_3'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
                                                        
                elif payload_received[i+6] == '4':
                    url = localhost_url + 'Temperature_sensor_inside_4'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
                                
                elif payload_received[i+6] == '5':
                    url = localhost_url + 'Temperature_sensor_solar_5'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
    
    if msg.topic == 'casenio/event/f8f005d87424/46/1/JSON':
        payload_received = msg.payload.decode("utf-8")
        #print(payload_received)
        for j in range(7, len(payload_received)):
            if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                payload = payload_received[7:j]
                break
        for i in range (53, len(payload_received)):
            if(payload_received[i:i+4] == "rssi"):
                #print(payload_received, payload_received[i+6:i+8])
                if payload_received[i+6] == '8':
                    url = localhost_url + 'Temperature_back_PVSys_8'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
                                                        
                elif payload_received[i+6] == '9':
                    url = localhost_url + 'Temperature_inside_PVSys_9'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
                                
                elif payload_received[i+6:i+8] == '10':
                    #print(payload_received[i+6:i+7])
                    url = localhost_url + 'Temperature_outside_PVSys_10'
                    headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
                    status = requests.post(url, headers=headers, data=payload)
                    #  uprint(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
                    if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                        print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                        # print("Error status is " + str(status_str))
                            
                
    
    for i in range(len(column)):
        if msg.topic == column[i]:
            payload_received = msg.payload.decode("utf-8")
            #print(payload_received)
            for j in range(7, len(payload_received)):
                if payload_received[j] == ',':
                    # print(i)
                    # print(payload_received[7:i])
                    payload = payload_received[7:j]
                    break
            # print(payload)

            url = localhost_url + openhab_item_names[i]
            # URL to publish or to send command to Wall-Plug  with payload OFF
            # print(payload + "for LEDSwitch")
            for itr in range(len(actuators)):
                if openhab_item_names[i] == actuators[itr]:
                    if payload == '0':
                        payload = 'OFF'
                    else:
                        payload = 'ON'

            headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}                
            status = requests.post(url, headers=headers, data=payload)
            #print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
            status_str = str(status)
            if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                # print("Error status is " + str(status_str))
            if openhab_item_names[i] == 'Luminance_Sensor_Luminance_1':
                url = localhost_url + 'Solar_radiation_1'
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
                payload = str(round(int(payload) * 0.0079,2))
                #print("solar radiation 1 " + payload)
                status = requests.post(url, headers=headers, data=payload)
                # print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
            
            if openhab_item_names[i] == 'Luminance_Sensor_Luminance_2':
                url = localhost_url + 'Solar_radiation_2'
                headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
                payload = str(round(int(payload) * 0.0079,2))
                #print("solar radiation 2 " + payload)
                status = requests.post(url, headers=headers, data=payload)
                # print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                status_str = str(status)
                
            for j in range(0, len(timestamps_items)):
                if openhab_item_names[i] == timestamps_items[j]:
                    url = localhost_url + timestamps_list[j]
                    now = datetime.now()
                    payload = now.strftime("%Y-%m-%d %H:%M:%S")
                    #print(payload + openhab_item_names[i])
                    status = requests.post(url, headers=headers, data=payload)
                    # print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                    status_str = str(status)
    
                            
                


# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("praeklima", "Praeklima2021")

# connect to HiveMQ Cloud on port 8883
client.connect("fb06b8022fb941089214e0f7b7025453.s1.eu.hivemq.cloud",
               8883, keepalive = 60)  # client.connect(<MQTT ip address/hostname>, <port number>)

# subscribe to the topics
for i in range(len(column)):
    client.subscribe(column[i])
client.subscribe('casenio/event/f8f005d87424/39/15/JSON')
client.subscribe('casenio/event/f8f005d87424/49/15/JSON')
client.subscribe('casenio/event/f8f005d87424/46/1/JSON')

client.subscribe('casenio/event/f8f005d87424/50/1/JSON')
client.subscribe('casenio/event/f8f005d87424/50/5/JSON')
client.subscribe('casenio/event/f8f005d87424/50/18/JSON')

def subscribe_mqtt():
    print("Subscribing feeds")
    for i in range(len(column)):
        client.subscribe(column[i])
    client.subscribe('casenio/event/f8f005d87424/39/15/JSON')
    client.subscribe('casenio/event/f8f005d87424/49/15/JSON')
    client.subscribe('casenio/event/f8f005d87424/46/1/JSON')
    client.subscribe('casenio/event/f8f005d87424/50/1/JSON')
    client.subscribe('casenio/event/f8f005d87424/50/5/JSON')
    client.subscribe('casenio/event/f8f005d87424/50/18/JSON')

# publish Data to the topic "my/LEDControl1_Switch"
# client.publish("casenio/event/f8f005d87424/16/302/JSON",
#                '{"int":0,"ts":"2021-06-21T13:36:26.000Z","pid":13136,"rssi":255,"fk_sensortypen":1026,"node":9}')

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
