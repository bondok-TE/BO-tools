from jnpr.junos import Device
from jnpr.junos.exception import *
import getpass
import json
import pandas as pd
from openpyxl import load_workbook,Workbook


def srx_interaction(device_ls):
    device_ls = []
    username = 'YOUR_USERNAME'
    response = ""
    for device in device_ls:
        hostname = device
        password = getpass.getpass(prompt=f"Enter password for {username}@{hostname}: ")
        # Connect to the device
        with Device(host=hostname, user=username, password=password) as dev:
            # Check if the connection is successfully established
            if dev.connected:
                print(f"Connected to {hostname}")
                
                # Send a command and retrieve the response
                command = 'show ntp status | display jason '
                response += dev.cli(command, format='text')
                
                # Print the response
                # print(response)
            else:
                print(f"Failed to connect to {hostname}")
    return response

def manipulate_response(response):
    # keys to include from the 
    
    keys_to_include = [
    "ntp-status.remote-server.hostname",
    "ntp-status.remote-server.device-ip",
    "ntp-status.remote-server.server-address",
    "ntp-status.remote-server.status",
    ]

    desired_order = [
        "hostname",
        "device-ip",
        "server-address",
        "status"
    ]

    # change string to dict

    data = json.loads(response)
    # add data to the response suitable for viewing in excel
    data["ntp-status"]["remote-server"][0]["hostname"] = "hostname"
    data["ntp-status"]["remote-server"][0]["device-ip"] = "ip"
    df = pd.json_normalize(data, record_path=['ntp-status', 'remote-server'], meta=keys_to_include,errors="ignore")

    # Reorder columns based on desired_order list

    df = df[desired_order]
    return df


def write_to_excel(df):
    
    workbook = Workbook()
    workbook.save("ntp_integrations.xlsx")
    file_path = 'ntp_integrations.xlsx'
    wb = load_workbook(file_path)
    sheet = wb.active
    # Rearrange columns in the DataFrame as per the desired order
    first_row = [
        "hostname",
        "device-ip",
        "server-address",
        "status"
    ]
    sheet.append(first_row)
    data_values = df.values.tolist()
    for row in data_values:
        sheet.append(row)
    wb.save("ntp_integrations.xlsx")
