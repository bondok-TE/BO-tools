from openpyxl import load_workbook


sheets = load_workbook("test.xlsx")
sheet = sheets.active
print(type(sheet))