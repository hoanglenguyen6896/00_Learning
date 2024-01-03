import PyPDF2

f = open('Working_Business_Proposal.pdf', 'rb')

"""
Read txt:
    - pdf_reader = PyPDF2.PdfFileReader(<your stream>)
    - page = pdf_reader.getPage(<page you need>)
    -
"""

pdf_reader = PyPDF2.PdfFileReader(f)
# print(pdf_reader.numPages)

page_one = pdf_reader.getPage(0)
page_two = pdf_reader.getPage(1)
page_one_txt = page_one.extractText()
# print(page_one_txt)

# Get a page and write to new pdf file
page_one = pdf_reader.getPage(0)
page_two = pdf_reader.getPage(1)
pdf_writer = PyPDF2.PdfFileWriter()
pdf_writer.addPage(page_one) # Can add another page
pdf_writer.addPage(page_two)

pdf_output = open('Some_BrandNew_Doc.pdf', 'wb')
pdf_writer.write(pdf_output)

pdf_txt = []

pdf_reader = PyPDF2.PdfFileReader(f)
for num in range(pdf_reader.numPages):
    page = pdf_reader.getPage(num)
    pdf_txt.append(page.extractText())
for index in pdf_txt:
    print(index)

pdf_output.close()
f.close()
