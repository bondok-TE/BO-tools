from netmiko import Netmiko
import concurrent.futures
import time 

start = time.perf_counter()

with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\pass.txt",'r')as file:
    password = file.read()

juniper_devices_ls = ['10.8.0.14','10.8.0.14','10.8.0.14','10.8.0.14','10.8.0.14','10.8.0.14','10.8.0.14']
fortinet_devices_ls = ['10.31.243.30','10.38.225.14']
paloalto_devices_ls = ['10.27.17.101 ','10.31.243.4']
# for sending many commands --> connection.send_config(list of strings)
def setup_device (device_type,ips):
    devices_ls = []
    for ip in ips:
        device = { 'host':ip,
                    'username': 'ahmed.k.gamal',
                    'password': password,
                    'device_type': device_type,
                    'port': 22
                   }
        devices_ls.append(device)
    return devices_ls
    
        
def fw_interaction(device,command):
 
    with Netmiko(**device) as connection:
        if device['device_type'] == 'paloalto_panos':
            response = connection.send_command(command,expect_string=r">")
        else:
            response = connection.send_command(command)
    return response

def juniper_interaction (juniper_devices,cmd):
    devices = setup_device('juniper',juniper_devices)
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = [exec.submit(fw_interaction,device,cmd) for device in devices]
        for res in results:
            print(res.result())

def fortinet_interaction (fortinet_devices,cmd):
    devices = setup_device('fortinet',fortinet_devices)
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = [exec.submit(fw_interaction,device,cmd) for device in devices]
        for res in results:
            print(res.result())

def paloalto_interaction (paloalto_devices,cmd):
    devices = setup_device('paloalto_panos',paloalto_devices)
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = [exec.submit(fw_interaction,device,cmd) for device in devices]
        for res in results:
            print(res.result())

# fw_interaction('fortinet',fortinet_devices_ls,'get system status')
# fw_interaction('paloalto_panos',paloalto_devices_ls,'show ntp')



end = time.perf_counter()
print(f'it takes {end-start} seconds')

