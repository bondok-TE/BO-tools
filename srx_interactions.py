from jnpr.junos import Device
from jnpr.junos.exception import *
import xml.etree.ElementTree as ET

pass_path = "D:\\coding_files\\pass.txt"
username = 'ahmed.k.gamal'

with open(pass_path,'r') as file:
    password = file.read()

def srx_interaction(hostip,fn):
    try:
        response = ""
        # password = getpass.getpass(prompt=f"Enter password for {username}@{hostname}: ")
        # Connect to the device
        with Device(host=hostip, user=username, password=password,port=22) as dev:
            # Check if the connection is successfully established
            if dev.connected:
                print(f"Connected to {hostip}")
                if fn == 5:
                    # Send a command and retrieve the response
                    response = dev.cli('show ntp association',format='json',warning=False)
                    hostname = dev.cli('show system information',warning=False)
                    hostname = list(map(str.split,hostname.split('\n')))[4][1]
                    # print(hostname)
                    # print(f"==============\n {response}")
                    # response = dev.rpc.get_ntp_status_information(ignore_warning = True)
                    # print(f"==============\n {response}")
                    # Print the response
                    # print("==============\n" + response)
                    return [response,hostname]
                elif fn == 6:
                    response = dev.rpc.get_ntp_associations_information()
                    mytree = ET.parse(response)
                    return mytree
            else:
                print(f"Failed to connect to {hostip}")
    except ConnectTimeoutError:
        print(f"connection time out to ip {hostip}")
    