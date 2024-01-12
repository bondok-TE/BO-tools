from openpyxl import load_workbook
import re
from openpyxl.styles import Font

def get_unsec() -> set:
    """
    Return unsecure ports as a set for fast searching
    """
    chk = ['20','21','23','25','80','8080','135','139','445','1433','3306','3389','110','143','161','389','5060','5900' ]
    return set(chk)

def read(data:dict) -> bool:
    """
    read data from excel, format it in dictionary ports{}, call the processing function
    params:
    data = {'fn_no': (int)function number,
            'excel_path': (str)path of excel file,
            'first_index': (str)index of the first cell containing port no.}

    """
    # read the excel file with the given path
    wb_list = load_workbook(data['excel_path'])

    # the selected sheet from the excel file is the active sheet
    sheet = wb_list.active

    """
    ports = {'e1': [(str)port1, port2, port3],
             'e2 : [(str)port1 .............],
             .....
             .....}
    """
    ports = {}

    # first index format ex: 'e2'
    first_row = int(data['first_index'][1:]) # first row is the number part ex: 2
    col_symbol = sheet[data['first_index'][0]] # first column is the letter part ex: e (only supported columns a-z)

    # loop on rows starting from the given index ex: 2, until the end of the column + 1 as the last element in range not included
    # acces each cell and get its data in a string format
    for row in range(first_row,len(col_symbol) + 1): 
        cell_index = data['first_index'][0] + str(row) # e2 e3 ....
        str_data = str(sheet[cell_index].value) # cell value

        # empty cells are neglected
        if str_data == 'None':
            continue
        else:
            # remove any alpha character in the cell
            ports[cell_index] = re.sub('[^a-zA-Z0-9]',' ', str_data).split()

    return processing(ports,sheet,wb_list,data['excel_path'])

def processing(cell_ports:dict,sheet,wb_list,file_path) -> bool:
    '''
    handles a to z columns in the excel file
    strings are included in port{} but not in get_unsec so neglected
    params:
    '''

    # get unsecure ports set
    chk = get_unsec()
    unsec_flag = 0 # no unsecure port detected, no insert happened before

    # loop on every element in the ports dict
    for cell_index,port_ls in cell_ports.items():
        inserted_index = chr( ord(cell_index[0]) + 1 ) + cell_index[1:]
        for port in port_ls:
            if port in chk:

                unsec_flag = unsec_flag_check(unsec_flag,sheet,cell_index)

                # if the inserted column empty, write directly
                if sheet[inserted_index].value is None:
                    sheet[inserted_index] =  port +"-->unsecure" 
                    sheet[inserted_index].font = Font(color="FF0000")
                
                # else append 
                else:
                    old_value = sheet[inserted_index].value
                    sheet[inserted_index] = old_value + "," + port + "-->unsecure" 
                    sheet[inserted_index].font = Font(color="FF0000")
                wb_list.save(file_path)

            elif port.lower() == "any":
                unsec_flag = unsec_flag_check(unsec_flag,sheet,cell_index)
                if sheet[inserted_index].value is None:
                    sheet[inserted_index] = "check_any" 
                    sheet[inserted_index].font = Font(color="FF0000")
                else:
                    old_value = sheet[inserted_index].value
                    sheet[inserted_index] = old_value +","+ port +"check_any" 
                    sheet[inserted_index].font = Font(color="FF0000")
                wb_list.save(file_path)
    if unsec_flag == 0:
        return False
    else:
        return True
        
def direct_chk(port:str):
    # will be changed to handle named protocols
    chk = get_unsec()
    if port in chk:
        print("unsecure, block it")
    else:
        print("secure, go ahead")

def unsec_flag_check(flag,sheet,cell_index):
    if flag == 0:
        # if no insert happened before, insert an empty column
        # @ letter - 97 = 0 (+1 indexing from 1) (+1 for the inserted column)
        sheet.insert_cols(idx = ord(cell_index[0]) - 95)
        return  1 # insertion happened
