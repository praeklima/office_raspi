from datetime import datetime
import openhab_data_access
import time

cloud_api_url = "https://praeklimatud%40gmail.com:praeklima_tud@2021@home.myopenhab.org/rest/items/"
localhost_url = "http://localhost:8080/rest/items/"
print('Overall_energy_consumption')
#yesterday = 50.68
#openhab_data_access.openhab_send_command(localhost_url, 'yesterday_overall_power', '121.2')
while 1:
    now = datetime.now()
    current_time = now.strftime("%H%M")
    yesterday = float(openhab_data_access.openhab_read_data(localhost_url, 'yesterday_overall_power'))
    E15 = float(openhab_data_access.openhab_read_data(localhost_url, 'Socket_Energy_1'))
    E16 = float(openhab_data_access.openhab_read_data(localhost_url, 'Socket_Energy_2'))
    E35 = float(openhab_data_access.openhab_read_data(localhost_url, 'Socket_Energy_3'))
    E36 = float(openhab_data_access.openhab_read_data(localhost_url, 'Socket_Energy_4'))
    E51 = float(openhab_data_access.openhab_read_data(localhost_url, 'Socket_Energy_51'))
    WB_Energy = float(openhab_data_access.openhab_read_data(localhost_url, 'Window_blinds_energy'))
    WO_Energy = float(openhab_data_access.openhab_read_data(localhost_url, 'Window_opening_energy'))
    SA_Energy = float(openhab_data_access.openhab_read_data(localhost_url, 'Slats_angle_energy'))

    Overall_energy_consumption = round(E15 + E16 + E35 + E36 + WB_Energy + WO_Energy + SA_Energy + E51, 3)
    
    if int(current_time) == 0000:
        yesterday = Overall_energy_consumption
        openhab_data_access.openhab_send_command(localhost_url, 'yesterday_overall_power', str(Overall_energy_consumption))
        
    if 00 <= int(current_time) <= 2359:
        today_energy_consumption = str(round(Overall_energy_consumption - yesterday, 3))
        openhab_data_access.openhab_send_command(localhost_url, 'Today_energy_consumption',today_energy_consumption)
    Overall_energy_consumption = str(Overall_energy_consumption)
    #print(Overall_energy_consumption)
    openhab_data_access.openhab_send_command(localhost_url, 'Overall_energy_consumption', Overall_energy_consumption)