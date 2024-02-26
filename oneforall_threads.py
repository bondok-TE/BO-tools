from netmiko import Netmiko
import concurrent.futures
import getpass
# juniper
# show system information | match hostname
# show chassis routing-engine | match uptime
# show chassis routing-engine | match Idle
# show system alarms

# forti
# get system performance status | grep Uptime
# get system performance status | grep CPU

# paloalto
# show system info | match hostname
# show system info | match uptime
# show system resources | match %Cpu
# show system state | match alarm


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
    :return: list of strings of ips
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
# for sending config commands --> connection.send_config_set(list of strings)
def _fw_interaction(device:dict,command_ls:list) -> str:
    """
    direct communication to any firewall using netmiko 
    :device: one element of _setup_device output list
    :command: list of commands to be sent to the firewall
    :return: the output of the sent command
    """
    with Netmiko(**device) as connection:
        response = ""
        if device['device_type'] == 'paloalto_panos':
            for command in command_ls:
                response += connection.send_command(command,expect_string=r">")
            return response
        elif device['device_type'] == 'fortinet' :
            config = ['config global'] + command_ls
            for command in config:
                response += connection.send_config_set(command)
            return response
        else:
            for command in command_ls:
                response += connection.send_command(command)
            return response

def _fw_interaction_batch(device:dict,command:list) -> str:
    with Netmiko(**device) as connection:
            if device['device_type'] == 'paloalto_panos':
                response = connection.send_config_set(command,expect_string=r">")
                return response
            elif device['device_type'] == 'fortinet' :
                response = connection.send_config_set(command)
                return response
            else:
                response = connection.send_config_set(command)
                return response    

# threading
def threads_interaction (device_type:str,username:str,password:str,cmd_ls:list )-> None:
    """
    call fw_interaction function through threads to boost the performance and handle the I/O waiting
    :device_type: OS type according to netmiko
    :cmd: list of commands to be sent to the firewall
    """
    devices = _setup_device(device_type,username,password)
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = [exec.submit(_fw_interaction,device,cmd_ls) for device in devices]
        for i in range(len(results)):
            print(devices[i]['host'],results[i].result(),sep='\n=============================\n')
            print("=============================")




# end = time.perf_counter()
# print(f'it takes {end-start} seconds')

