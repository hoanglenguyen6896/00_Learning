import csv
import PyPDF2
import re

data = open('D:\\Libraries\\Documents\\Python\\17_pdf_csv\\Exercise_Files\\find_the_link.csv', encoding = 'utf-8')
csv_data = csv.reader(data)

data_lines = list(csv_data)
gg_link = ''
rows = len(data_lines)

for row in range(rows):
    gg_link += data_lines[row][row]

print(gg_link)



data = open('D:\\Libraries\\Documents\\Python\\17_pdf_csv\\Exercise_Files\\Find_the_Phone_Number.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(data)
# Method 1
pattern = r'(\d\d\d\W\d\d\d\W\d\d\d\d)'
pdf_txt = ''
for num in range(pdf_reader.numPages):
    page = pdf_reader.getPage(num)
    pdf_txt += page.extractText()
result = re.search(pattern, pdf_txt)
print(result.group())

# Method 2
new_pat = r'(\d\d\d)'
for match in re.finditer(new_pat, pdf_txt):
    print(match)
print(pdf_txt[41794:41794+20])