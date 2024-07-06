from openpyxl import load_workbook
from threading import Thread

def write_to_xlsx(cell, value, sheet_obj):
    sheet_obj[cell] = value

workbook_name = 'sample.xlsx'
wb = load_workbook(workbook_name)
page = wb.active

thr = []
a = ['A1', 'A2', 'A10', 'A11']
i = 123123
for cell in a:
    t = Thread(target = write_to_xlsx, args = (cell, i, page))
    t.start()
    thr.append(t)
    i += 1

for t in thr:
    t.join()

wb.save(filename=workbook_name)