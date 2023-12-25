from jnpr.junos import Device
from jnpr.junos.exception import *
import json
import pandas as pd
import pprint as pp
from openpyxl import load_workbook,Workbook


pass_path = "C:\\Users\\Ahmed.K.Gamal\\Desktop\\pass.txt"
username = 'ahmed.k.gamal'

with open(pass_path,'r') as file:
    password = file.read()

def srx_interaction(device):
    response = ""
    hostname = device
    # password = getpass.getpass(prompt=f"Enter password for {username}@{hostname}: ")
    # Connect to the device
    with Device(host=hostname, user=username, password=password,port=22) as dev:
        # Check if the connection is successfully established
        if dev.connected:
            print(f"Connected to {hostname}")
            
            # Send a command and retrieve the response
            command = 'show ntp association'
            response = dev.cli(command, format='json')
            print(f"==============\n {response}")
            # response = dev.rpc.get_ntp_status_information(ignore_warning = True)
            # print(f"==============\n {response}")
            
            # Print the response
            # print("==============\n" + response)
        else:
            print(f"Failed to connect to {hostname}")
    return response

def dct_ntp_association(ntp_association):
    ntp_association_val = ntp_association['output'][0]['data'].split('\n')
    ntp_association_val.pop(1)
    ntp_association_val = list(map(str.split,ntp_association_val))
    response = {"data":[]}
    ntp_association_val_dct_1 = {}
    ntp_association_val_dct_2 = {}
    for ind,val in enumerate(ntp_association_val[0]):
        ntp_association_val_dct_1[val] = (ntp_association_val[1][ind])
        ntp_association_val_dct_2[val] = (ntp_association_val[2][ind])
    
    response['data'].append(ntp_association_val_dct_1)
    response['data'].append(ntp_association_val_dct_2)

    # pp.pprint(ntp_association_val_dct_1)
    # print("===========")
    # pp.pprint(ntp_association_val_dct_2)
    # print("===========")
    # pp.pprint(response)


    return response

def manipulate_response(response):
    # keys to include from the 
    
    # keys_to_include = [
    # "ntp-status.remote-server.hostname",
    # "ntp-status.remote-server.device-ip",
    # "ntp-status.remote-server.server-address",
    # "ntp-status.remote-server.status",
    # ]

    desired_order = [
        "hostname",
        "device-ip",
        "remote",
        "refid",
        "st",
        "t",
        "when",
        "poll",
        "reach",
        "delay",
        "offset",
        "jitter"
    ]

    # add data to the response suitable for viewing in excel
    response['data'][0]["hostname"] = "hostname"
    response['data'][0]["device-ip"] = "ip"
    df = pd.json_normalize(response,record_path=['data'],errors="ignore")

    # Reorder columns based on desired_order list

    df = df[desired_order]
    # print(df)
    return df


def create_excel():
    workbook = Workbook()
    workbook.save("ntp_integrations.xlsx")
    file_path = 'ntp_integrations.xlsx'
    wb = load_workbook(file_path)
    sheet = wb.active
    first_row = [
        "hostname",
        "device-ip",
        "remote",
        "refid",
        "st",
        "t",
        "when",
        "poll",
        "reach",
        "delay",
        "offset",
        "jitter"
    ]
    sheet.append(first_row)
    return [wb,sheet]

def write_to_excel(wb_sheet,df):
    wb = wb_sheet[0]
    sheet = wb_sheet[1]
    data_values = df.values.tolist()
    for row in data_values:
        sheet.append(row)
    wb.save("ntp_integrations.xlsx")