from netmiko import Netmiko
import concurrent.futures
import getpass
# import time 

# start = time.perf_counter()

# credintials
# with open("D:\\coding_files\\pass.txt",'r')as file:
#     password = file.read()

def _file_content(device:str) -> list :  
    """
    called by _setup_device function to open a text file and return its content as string, the file should not contain any empty lines
    :devices: the device OS type the input is the same name used for this OS in netmiko and also the same as the file.txt naming 
              the file.txt should contain the ips of all devices of this OS
    :return: list of strings og ips
    """
    with open(f"D:\\coding_files\\one_for_all_{device}.txt")as file:
        return file.read().split("\n") 

def _setup_device (device_type:str,username:str,password:str) -> list:
    """
    called by thread_interaction to create a dict of the needed data to be used by netmiko
    :user: login username
    :password: 
    :device_type: OS type according to netmiko
    :return: list of dicts
    """
    ips = _file_content(device_type)
    devices_ls = []
    for ip in ips:
        device = {  'host':ip,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'port': 22
                }
        devices_ls.append(device)
    return devices_ls

# direct communication with any fw
# for sending config commands --> connection.send_config(list of strings)
def _fw_interaction(device:dict,command:str) -> str:
    """
    direct communication to any firewall using netmiko 
    :device: one element of _setup_device output list
    :command: command to be sent to the firewall
    :return: the output of the sent command
    """
    with Netmiko(**device) as connection:
        if device['device_type'] == 'paloalto_panos':
            response = connection.send_command(command,expect_string=r">")
        else:
            response = connection.send_command(command)
    return response

# threading
def threads_interaction (device_type:str,username:str,password:str,cmd:str )-> None:
    """
    call fw_interaction function through threads to boost the performance and handle the I/O waiting
    :device_type: OS type according to netmiko
    :cmd: command to be sent to the firewall
    """
    devices = _setup_device(device_type,username,password)
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = [exec.submit(_fw_interaction,device,cmd) for device in devices]
        for i in range(len(results)):
            print(devices[i]['host'],results[i].result(),sep='\n=============================')
            print("=============================")




# end = time.perf_counter()
# print(f'it takes {end-start} seconds')

