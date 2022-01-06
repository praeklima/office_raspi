import paho.mqtt.client as mqtt
import requests
import time
import sys
from datetime import datetime

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"

# Dictonary of MQTT Feeds/topics, add the topics of the broker in this Dictonary
column = ['sensor/switch/f8f005d87424/15/302/JSON', 'sensor/switch/f8f005d87424/16/302/JSON',
          'sensor/switch/f8f005d87424/35/302/JSON', 'sensor/switch/f8f005d87424/36/302/JSON',
          'sensor/switch/f8f005d87424/51/302/JSON',
          'sensor/switch/f8f005d87424/57/327/JSON', 'sensor/switch/f8f005d87424/50/598/JSON', 'sensor/switch/f8f005d87424/50/599/JSON','sensor/switch/f8f005d87424/53/328/JSON',
          'sensor/switch/f8f005d87424/53/327/JSON', 'sensor/switch/f8f005d87424/56/327/JSON'
          ]

# Openhab items, where the MQTT topics data is to be stored on Openhab items, "place the list in the same order as MQTT topics"
openhab_item_names = ['Socket_Switch_1', 'Socket_Switch_2', 'Socket_Switch_3', 'Socket_Switch_4', 'Socket_Switch_51', 'Ventilation_Flap',
                      'Lunos_Ventilation_Mode', 'Lunos_Ventilation_Heat_Recovery_mode',
                      'Slats_angle', 'Window_blinds', 'Window_opening_angle']
openhab_values = []


actuators = ['Socket_Switch_1', 'Socket_Switch_2', 'Socket_Switch_3', 'Socket_Switch_4', 'Socket_Switch_51',
             'Ventilation_Flap_switch', 'Window_blinds', 'Window_opening_angle']

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
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

def on_publish(client, userdata, mid):
    #print("mid:" + str(mid))
    pass


# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish 

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("praeklima", "Praeklima2021")

# connect to HiveMQ Cloud on port 8883
client.connect("fb06b8022fb941089214e0f7b7025453.s1.eu.hivemq.cloud",
               8883, keepalive=60)  # client.connect(<MQTT ip address/hostname>, <port number>)

# subscribe to the topics
#for i in range(len(column)):
#    client.subscribe(column[i])

for i in range(0, len(openhab_item_names)):
    if(i >= 5):
        openhab_values.append('0')
    else:
        openhab_values.append('OFF')
        
for i in range(0, 4):
    url = localhost_url + openhab_item_names[i] + "/state"  # accessing data from items
    res = requests.get(url)
    value = res.text
    #print(value + " " + openhab_item_names[i])
        #if openhab_item_names[i] == 'Window_blinds' or openhab_item_names[i] == 'Window_opening_angle':
    #if (value != openhab_values[i]):
    openhab_values[i] = value
    #value1 = '{"value": "'+ value+ '"}'
    #client.publish(column[i], value1)

#print(openhab_values)
        
        
while True:
    client.loop_start()
    now = datetime.now()
    #sys.stdout.write("\r")
    #print(now.strftime("%Y-%m-%d %H:%M:%S"), end='', flush=True)
    for i in range(0, len(openhab_item_names)):
        url = localhost_url + openhab_item_names[i] + "/state"  # accessing data from items
        res = requests.get(url)
        value = res.text
        #print(value + " " + openhab_item_names[i])
        #if openhab_item_names[i] == 'Window_blinds' or openhab_item_names[i] == 'Window_opening_angle':
        sys.stdout.write("\r")
        print(openhab_values, now.strftime("%Y-%m-%d %H:%M:%S"), end='', flush=True)
        if i >= 5:
            
            if (value != openhab_values[i]):
                #print("I am here")
                #print(openhab_item_names[i], value, openhab_values[i])
                openhab_values[i] = value
                if openhab_item_names[i] == 'Ventilation_Flap' and value == 'Summer':
                    value1 = '{"value": "'+ '99'+ '"}'
                elif openhab_item_names[i] == 'Ventilation_Flap' and (value == 'Winter' or value == 'NULL'):
                    value1 = '{"value": "'+ '0'+ '"}'
                else:
                    value = float(value)
                    value = int(value)
                    value1 = '{"value": "'+ str(value)+ '"}'
                    #openhab_values[i] = str(value)
                client.publish(column[i], value1)
                #print(openhab_item_names[i] + column[i] + value1)
        else:
            #print(value)
            if (value != openhab_values[i]):
                if value == 'ON':
                    openhab_values[i] = 'ON'
                    #print(openhab_values)
                    value1 = '{"value": "1"}'
                    client.publish(column[i], value1)
                    #print(openhab_item_names[i] + column[i] + value1)
                else:
                    openhab_values[i] = 'OFF'
                    value1 = '{"value": "0"}'
                    client.publish(column[i], value1)
                    #print(openhab_item_names[i] + column[i] + value1)
           
        #print(value)
        #client.publish(column[i], value)
       
    time.sleep(5)
    client.loop_stop()

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
#client.loop_forever()

