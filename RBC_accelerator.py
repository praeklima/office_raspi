
from datetime import datetime
import openhab_data_access
import sys
import time

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"

while True:
    
    control_Algorithm = openhab_data_access.openhab_read_data(localhost_url, 'Control_Algorithm')
    #print(control_Algorithm)
    if control_Algorithm == "Manual":
        sys.stdout.write("\r")
        print("Algorithm: Manual - Do Nothing", end='', flush=True)
    elif control_Algorithm == "RBC_V1":
        sys.stdout.write("\r")
        print("Algorithm: RBC_V1", end='', flush=True)
        now = datetime.now()
        current_time = now.strftime("%H%M")

        occupancy1 = openhab_data_access.openhab_read_data(localhost_url, 'Brightness_Sensor_Motion_detection_1')
        occupancy2 = openhab_data_access.openhab_read_data(localhost_url, 'Brightness_Sensor_Motion_detection_2')
        occupancy = occupancy1 == 'ON' or occupancy2 == 'ON'

        #Tout = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Temperature_1'))
        vt14 = float(openhab_data_access.openhab_read_data(localhost_url, 'Enocean_Temperature_1'))
        vt22 = float(openhab_data_access.openhab_read_data(localhost_url, 'AIR_Quality_Sensor_Temperature_2'))
        vt21 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Temperature_1'))
        vt40 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Temperature_3'))
        Tout = round((vt14 + vt22 + vt21 + vt40)/4, 2)

        vh14 = float(openhab_data_access.openhab_read_data(localhost_url, 'Enocean_Humidity_1'))
        vh22 = float(openhab_data_access.openhab_read_data(localhost_url, 'AIR_Quality_Sensor_Humidity_2'))
        vh21 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Humidity_1'))
        vh40 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Humidity_3'))
        RHout = round((vh40 + vh22 + vh21 + vh14)/4, 2)

        vt12 = float(openhab_data_access.openhab_read_data(localhost_url, 'Brightness_sensor_temperature_1'))
        #vt13 = float(openhab_data_access.openhab_read_data(localhost_url, 'Brightness_Sensor_Temperature_2'))
        vt20 = float(openhab_data_access.openhab_read_data(localhost_url, 'AirQualitySensor_SensorTemperature'))
        vt25 = float(openhab_data_access.openhab_read_data(localhost_url, 'Temperature_25'))
        vt27 = float(openhab_data_access.openhab_read_data(localhost_url, 'Temperature_27'))
        vt24 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Temperature_2'))
        Tin = round((vt12 + vt20 + vt25 + vt27 + vt24)/5, 2)

        vh20 = float(openhab_data_access.openhab_read_data(localhost_url, 'AirQualitySensor_SensorRelativeHumidity'))
        vh24 = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Humidity_2'))
        RHin = round((vh20 + vh24)/2, 2)

        Tcold = 18
        Toptimal = 24.5
        Tdew = float(openhab_data_access.openhab_read_data(localhost_url, 'Weather_Station_Dew_Point_1'))
        Tlimit = 17

        RHlimit = 70
        Tlow = 21
        summer_winter_flap = openhab_data_access.openhab_read_data(localhost_url, 'Ventilation_Flap_switch')

        lux_inside = int(float(openhab_data_access.openhab_read_data(localhost_url, 'Luminance_Sensor_Luminance_2')))
        lux_outside = float(openhab_data_access.openhab_read_data(localhost_url, 'Luminance_Sensor_Luminance_1'))
        lux_min = 500
        lux_max = 3000

        Heater = openhab_data_access.openhab_read_data(localhost_url, 'Socket_Switch_2')
        CO2 = int(float(openhab_data_access.openhab_read_data(localhost_url, 'AirQualitySensor_SensorCO2')))

        # Blinds RBC Algorithm
        if occupancy == 'OFF':
            if 600 <= int(current_time) <= 1900:
                if Heater == 'ON':
                    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '99')
                else:
                    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '0')
            else:
                if Heater == 'ON':
                    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '0')
                else:
                    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '99')
        else:
            if lux_outside <= lux_max:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '99')
                time.sleep(30)
                com1 = openhab_data_access.openhab_send_command(localhost_url, 'Slats_angle', '45')
            elif 10000 > lux_outside > 3000:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '0')
                time.sleep(30)
                com1 = openhab_data_access.openhab_send_command(localhost_url, 'Slats_angle', '45')
            else:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Window_blinds', '0')
                time.sleep(30)
                com1 = openhab_data_access.openhab_send_command(localhost_url, 'Slats_angle', '99')

        # Window natural Ventilation RBC Algorithm

        current_position = int(openhab_data_access.openhab_read_data(localhost_url, 'Window_opening_angle'))
        #print(Tcold, Tdew)
        if Tcold < Tout < Toptimal and Tdew < Tlimit:
            print("window opening in if case", end='', flush=True)
            com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '99')
        else:
            if int(current_time) == 900 or int(current_time) == 1200 or int(current_time) == 1500:
                print("window opening in schedule", end='', flush=True)
                if int(current_time)%100 < 5:
                    if current_position != 99:
                        com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '99')
                
            else:
                print("    window is closed", end='', flush=True)
                if current_position != 0:
                    com = openhab_data_access.openhab_send_command(localhost_url, 'Window_opening_angle', '0')

        # preheat/precool based on winter/summer flap
        #if summer_winter_flap == 'ON':
        #    if Tin < Tlow:
        #        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'ON')
        #    else:
        #        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'OFF')
        #else:
        #    if Tin > Toptimal or RHin > RHlimit:
        #        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'ON')
        #    else:
        #        openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_2', 'OFF')

        if 600 <= int(current_time) <= 1900:
            #print(" Lunos Mode active time ", int(current_time))
            #Artifitial lighting control
            #if lux_inside < 500:
            #    openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_51', 'ON')
            #elif lux_inside > 6000:
            #    openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_51', 'OFF')
            
            #Lunos Ventilation mode control as per occupency currently 0.5
            if int(current_time)%100 < 41:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Mode', '2')
            else:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Mode', '0')
        else:
            #openhab_data_access.openhab_send_command(localhost_url, 'Socket_Switch_51', 'OFF')
            #print(" Lunos Mode inactive time") 
            if int(current_time)%100 < 2:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Mode', '1')
            else:
                com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Mode', '0')
                
                
        if Tout < Tin and Tin < 25:
            com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Heat_Recovery_mode', '2')
        else:
            com = openhab_data_access.openhab_send_command(localhost_url, 'Lunos_Ventilation_Heat_Recovery_mode', '1')
    
    elif control_Algorithm == "RL_V1":
        sys.stdout.write("\r")
        print("Control Algorithm is RL_V1", end='', flush=True)
    time.sleep(5)   






