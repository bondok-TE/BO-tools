from automation import *
print('================ Welcome to BO_tools ================\n')
while(True):
    excel_data = get_data()
    if excel_data['fn_no'] == 0:
        break
    elif excel_data['fn_no'] == 1:
        unsecure_ports_check(excel_data)
        print("==================================================")
    elif excel_data['fn_no'] == 2:
        direct_chk(input("input the port number"))
        print("==================================================")

