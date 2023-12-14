from automation import *
from new_policy import *
from ntp_integration import *

print('================ Welcome to BO_tools ================3')
while(True):
    fn_no = int(input('''Pleased input the function number
0 --> exit the program
1 --> xlsx unsecure ports check
2 --> shell unsecure ports check
3 --> create new policy
4 --> srx ntp integration\n'''))
    
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
        srx_ips = input("input ips of srx devices").split()
        response = srx_interaction(srx_ips)
        data_frame = manipulate_response(response)
        write_to_excel(data_frame)
        

