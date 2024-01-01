from automation import *
from new_policy import *
from ntp_integration import *
from srx_interactions import *
print('================ Welcome to BO_tools ================3')
while(True):
    print('Pleased input the function number:')
    print("0 --> exit the program")
    print("1 --> xlsx unsecure ports check")
    print("2 --> shell unsecure ports check")
    print("3 --> create srx new policy beginner mode")
    print("4 --> create srx new policy advanced mode")
    print("5 --> srx ntp integration")
    print("6 --> srx pull OS")

    fn_no = int(input())
    
    if fn_no == 0:
        break
    elif fn_no == 1:
        data = {}
        print("Please make sure to close the excel file not to get any errors")
        excel_path = input("""Please input the excel file path with its extension just the .xlsx file name if the file in the same dir as this script else input the abs path\n""")
        first_index = input("Please input the index of the first port ex: L5\n")
        data['fn_no'] = fn_no
        data['excel_path'] = excel_path
        data['first_index'] = first_index
        unsec_findings = excel_auto(data)
        if unsec_findings == 0:
            print("There isn't any unsecure ports in your file, go ahead!\n")
        else:
            print("Ops, I found some unsecure stuff, go check them\n")
        print("==================================================")
    elif fn_no == 2:
        direct_chk(input("input the port number\n"))
        print("==================================================")
    elif fn_no == 3:
        print("===============Welcome to Juniper policy wizard===============")
        print("1-start with the source ip(s) or subnet(s)")
        src_ip_ls = input("input the src ip(s) or src subnet(s)\n").split()
        src_zone_adset = obj_ip(src_ip_ls,"source")
        print("2-Then we do the same for the destination ip(s) or subnet(s)")
        dst_ip_ls = input("input the dst ip(s) or dst subnet(s)\n").split()
        dst_zone_adset = obj_ip(dst_ip_ls,"destination")
        print("3-Now the ports trun")
        src_ports_chk = input("are source ports specified? yes-->1 no-->0\n")
        if int(src_ports_chk):
            src_ports_ls = input("input the src port(s)\n").split()
            src_app_group = port_obj( src_ports_ls,"source")
        else:
            src_app_group = ["any"]
        dst_ports_chk = input("are destination ports specified? yes-->1 no-->0\n")
        if int(dst_ports_chk):
            dst_ports_ls = input("input the dst port(s)\n").split()
            dst_app_group = port_obj( dst_ports_ls,"destination")
        else:
            dst_app_group = ["any"]
        print("4-Finally we create the policy")
        create_policy(src_zone_adset, dst_zone_adset, src_app_group, dst_app_group)
    elif fn_no == 4:
        file_path = input('in the advanced mode you give me a file path with policy params, i give you the policy cmds, fair enough huh?\n') 
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                try:
                    policy_params = json.loads(file_content)
                    # print(policy_params)
                    create_policy(policy_params["src_zone_adset"], policy_params["dst_zone_adset"], policy_params["src_app_group"], policy_params["dst_app_group"])
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except IOError:
            print(f"Error reading file '{file_path}'.")
    elif fn_no == 5:
        devices = "devices.txt"
        with open(devices,'r')as file:
            srx_ips = file.read().split("\n")
        wb_sheet = create_excel()
        for ip in srx_ips:
            response,hostname = srx_interaction(ip,fn_no)
            if response == "":
                break
            ntp_association_dct = dct_ntp_association(response)
            data_frame = manipulate_response(ntp_association_dct,ip,hostname)
            write_to_excel(wb_sheet,data_frame)
        if response != "":
            print("integration report is created check ./ntp_integrations.xlsx")
    elif fn_no == 6:
        pass
        

