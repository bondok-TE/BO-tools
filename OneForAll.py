from netmiko import Netmiko

with open("C:\\Users\\Ahmed.K.Gamal\\Desktop\\pass.txt",'r')as file:
    password = file.read()

juniper_devices_ls = ['10.8.0.14','10.33.128.14']
fortinet_devices_ls = ['10.31.243.30','10.38.225.14']
paloalto_devices_ls = ['10.27.17.101 ','10.31.243.4']
# for sending many commands --> connection.send_config(list of strings)
def fw_interaction(device_type,ips,command):
    response= []
    for ip in ips:
        devices = { 'host':ip,
                    'username': 'ahmed.k.gamal',
                    'password': password,
                    'device_type': device_type,
                    'port': 22
                    }
        connection = Netmiko(**devices)
        if device_type == 'paloalto_panos':
            res = connection.send_command(command,expect_string=r">")
            
        else:
            res = connection.send_command(command)
        response.append(res)
    print(*response,'#'*20,sep="\n")

# fw_interaction('juniper',juniper_devices_ls,'show ntp association')
# fw_interaction('fortinet',fortinet_devices_ls,'get system status')
# fw_interaction('paloalto_panos',paloalto_devices_ls,'show ntp')

