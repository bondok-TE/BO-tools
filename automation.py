from openpyxl import workbook, load_workbook
import re
from openpyxl.styles import Font

def get_unsec():
    chk = ['20','21','23','25','80','8080','135','139','445','1433','3306','3389','110','143','161','389','5060','5900' ]
    return set(chk)

def get_data():

    my_data = dict()
    fn_no = int(input('''Pleased input the function number
0 --> exit the program
1 --> xlsx unsecure ports check
2 --> shell unsecure ports check\n'''))

    if fn_no == 0:
        my_data["fn_no"] = 0
        return my_data
    elif fn_no == 1:
        print("Please make sure to close the excel file not to get any errors\n")
        my_data['fn_no'] = int(fn_no)
        my_data['excel_path'] = input("""Please input the excel file path, just the .xlsx file name if the file in the same dir as this scripts, else input the abs path\n""")
        # my_data['sheet_name'] = input("Please input the sheet number\n")
        my_data['first_index'] = input("Please input the index of the first port ex: L5\n")
        return my_data
    elif fn_no == 2:
        pass 

def unsecure_ports_check(data:dict):
    read(data)

def read(data:dict):
    wb_list = load_workbook(data['excel_path'])
    # sheet = wb_list[data['sheet_name']] 
    sheet = wb_list.active
    ports = {}
    for i in range(int(data['first_index'][1:]),len(sheet[data['first_index'][0]])+1): 
        '''
        A15
        first part of the range 15
        second part of the range len of this column
        '''
        str_data = str(sheet[data['first_index'][0] + str(i)].value)
        if str_data == 'None':
            continue
        else:
            ports[data['first_index'][0] + str(i)] = re.sub('[^a-zA-Z0-9]',' ', str_data).split()
    # print(ports)
    processing(ports,sheet,wb_list)

def processing(ports,sheet,wb):
    '''
    handles max z columns in the excel file
    '''
    chk = get_unsec()
    unsec_flag = 0
    for i,k in ports.items():
        for j in k:
            if j in chk:
                if unsec_flag == 0:
                    sheet.insert_cols(idx = ord(i[0]) - 95)
                    unsec_flag = 1
                sheet[chr( ord(i[0]) + 1 ) + i[1:]] = "unsecure" 
                sheet[chr( ord(i[0]) + 1 ) + i[1:]].font = Font(color="FF0000")
                wb.save('test.xlsx')
            elif j.lower() == "any":
                if unsec_flag == 0:
                    sheet.insert_cols(idx = ord(i[0]) - 95)
                    unsec_flag = 1
                sheet[chr( ord(i[0]) + 1 ) + i[1:]] = "check any!" 
                sheet[chr( ord(i[0]) + 1 ) + i[1:]].font = Font(color="FFFF00")
                wb.save('test.xlsx')
    if unsec_flag == 0:
        print("There is not unsecure ports in your file, go ahead!\n")
    else:
        print("Ops, I found some unsecure stuff, go check them\n")
        
def direct_chk(port):
    chk = get_unsec
    if port in chk:
        print("unsecure, block it")
    else:
        print("secure, go ahead")


