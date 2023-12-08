from openpyxl import workbook, load_workbook
import re
from openpyxl.styles import Font

def get_unsec():
    chk = ['20','21','23','25','80','8080','135','139','445','1433','3306','3389','110','143','161','389','5060','5900' ]
    return set(chk)

def excel_auto(my_data):
    return read(my_data)

def read(data:dict):
    wb_list = load_workbook(data['excel_path'])
    # sheet = wb_list[data['sheet_name']] 
    sheet = wb_list.active
    ports = {}
    first_row = int(data['first_index'][1:])
    col_symbol = sheet[data['first_index'][0]]
    for i in range(first_row,len(col_symbol) + 1): 
        cell_index = data['first_index'][0] + str(i)
        str_data = str(sheet[cell_index].value)
        if str_data == 'None':
            continue
        else:
            # will be changed to handle named protocols
            ports[cell_index] = re.sub('[^a-zA-Z0-9]',' ', str_data).split()

    return processing(ports,sheet,wb_list,data['excel_path'])

def processing(ports,sheet,wb,file):
    '''
    handles a to z columns in the excel file
    strings are included in port{} but not in get_unsec so neglected
    '''
    chk = get_unsec()
    unsec_flag = 0
    for i,k in ports.items():
        inserted_index = chr( ord(i[0]) + 1 ) + i[1:]
        for j in k:
            if j in chk:
                new_port = j
                if unsec_flag == 0:
                    sheet.insert_cols(idx = ord(i[0]) - 95)
                    unsec_flag = 1
                if sheet[inserted_index].value is None:
                    sheet[inserted_index] =  new_port +"-->unsecure" 
                    sheet[inserted_index].font = Font(color="FF0000")
                else:
                    old_value = sheet[inserted_index].value
                    sheet[inserted_index] = old_value + "," + new_port + "-->unsecure" 
                    sheet[inserted_index].font = Font(color="FF0000")
                wb.save(file)
            elif j.lower() == "any":
                if unsec_flag == 0:
                    sheet.insert_cols(idx = ord(i[0]) - 95)
                    unsec_flag = 1
                if sheet[inserted_index].value is None:
                    sheet[inserted_index] = "check_any" 
                    sheet[inserted_index].font = Font(color="FF0000")
                else:
                    old_value = sheet[inserted_index].value
                    sheet[inserted_index] = old_value +","+ j +"check_any" 
                    sheet[inserted_index].font = Font(color="FF0000")
                wb.save(file)
    if unsec_flag == 0:
        return 0
    else:
        return 1
        
def direct_chk(port):
    # will be changed to handle named protocols
    chk = get_unsec()
    if port in chk:
        print("unsecure, block it")
    else:
        print("secure, go ahead")

def create_policy():
    pass
