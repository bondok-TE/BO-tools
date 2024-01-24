from jnpr.junos import Device
from jnpr.junos.exception import *

pass_path = "C:\\Users\\Ahmed.K.Gamal\\Desktop\\pass.txt"
username = 'ahmed.k.gamal'

with open(pass_path,'r') as file:
    password = file.read()

def srx_interaction(hostip,fn,ip):
    try:
        response = ""
        # password = getpass.getpass(prompt=f"Enter password for {username}@{hostname}: ")
        # Connect to the device
        with Device(host=hostip, user=username, password=password,port=22) as dev:
            # Check if the connection is successfully established
            if dev.connected:
                print(f"Connected to {hostip}")
                print(f"for {ip}\n================================")
                if fn == 5:
                    # Send a command and retrieve the response
                    response = dev.cli(f'show route {ip}',format='text',warning=False)
                    # hostname = dev.cli('show system information',warning=False)
                    # hostname = list(map(str.split,hostname.split('\n')))[4][1]
                    # print(hostname)
                    # print(f"==============\n {response}")
                    # response = dev.rpc.get_ntp_status_information(ignore_warning = True)
                    # print(f"==============\n {response}")
                    
                    # Print the response
                    # print("==============\n" + response)
                    return response
                elif fn == 6:
                    pass
            else:
                print(f"Failed to connect to {hostip}")
    except ConnectTimeoutError:
        print(f"connection time out to ip {hostip}")

ips = ["41.222.132.235",
"41.222.132.237",
"41.222.132.236",
"41.222.132.238",
"41.222.132.235",
"41.222.132.237",
"41.222.132.236",
"41.222.132.238"]

for ip in ips:
    print(srx_interaction("10.8.0.14",5,ip))
    print("================================================")