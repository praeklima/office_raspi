import paho.mqtt.client as mqtt
import requests
import time
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
          'casenio/event/f8f005d87424/17/69/JSON', 'casenio/event/f8f005d87424/18/69/JSON',
          'casenio/event/f8f005d87424/17/602/JSON', 'casenio/event/f8f005d87424/18/602/JSON',
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
          'casenio/event/f8f005d87424/21/6/JSON','casenio/event/f8f005d87424/23/12/JSON', 
          'casenio/event/f8f005d87424/23/202/JSON', 'casenio/event/f8f005d87424/23/602/JSON',
          'casenio/event/f8f005d87424/25/1/JSON', 'casenio/event/f8f005d87424/26/1/JSON',
          'casenio/event/f8f005d87424/27/1/JSON']

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
                      'Weather_Station_Temperature_1', 'Weather_Station_Wind_Speed_1',
                      'Rain_Sensor_Precipitation_2', 'Rain_Sensor_Water_Meter_2', 'Rain_Sensor_Battery_2',
                      'Temperature_25', 'Temperature_26', 'Temperature_27', 'Ventilation_Flap_switch',
                      'Window_blinds', 'Window_opening_angle']

actuators = ['Ventilation_Flap_switch', 'Socket_Switch_1', 'Socket_Switch_2', 'Socket_Switch_3', 'Socket_Switch_4','Brightness_Sensor_Motion_detection_1', 'Brightness_Sensor_Motion_detection_2']

timestamps_list = ['AIR_Quality_Sensor_CO2_2_time_stamp', 'AIR_Quality_Sensor_CO2_1_time_stamp']
timestamps_items = ['AIR_Quality_Sensor_CO2_2', 'AirQualitySensor_SensorCO2']
print("PAHO_MQTT")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


payload = 0


# The callback for when a PUBLISH message is received from the server.
# Callback Definition: subscribed topics data will be received and will commit that data to the respective openhab item
def on_message(client, userdata, msg):
    global payload
    # print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    for i in range(len(column)):
        if msg.topic == column[i]:
            payload_received = msg.payload.decode("utf-8")
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
            # print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
            status_str = str(status)
            if status_str[len(status_str) - 5:len(status_str) - 2] != "200":
                print(openhab_item_names[i] + " set to " + payload + ": " + str(status))
                # print("Error status is " + str(status_str))
            
            for j in range(0, len(timestamps_items)):
                if openhab_item_names[i] == timestamps_items[j]:
                    url = localhost_url + timestamps_list[j]
                    payload = str(datetime.now())
                    print(payload + openhab_item_names[i])
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
               8883)  # client.connect(<MQTT ip address/hostname>, <port number>)

# subscribe to the topics
for i in range(len(column)):
    client.subscribe(column[i])

# publish Data to the topic "my/LEDControl1_Switch"
# client.publish("casenio/event/f8f005d87424/16/302/JSON",
#                '{"int":0,"ts":"2021-06-21T13:36:26.000Z","pid":13136,"rssi":255,"fk_sensortypen":1026,"node":9}')

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
