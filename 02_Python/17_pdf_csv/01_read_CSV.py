import csv

# open file
data = open('example.csv', encoding = 'utf-8')

# call csv.reader
csv_data = csv.reader(data)

# reformat to a python object, maybe a list of list
data_lines = list(csv_data)

# print(data_lines[0])
# print(len(data_lines))

# for line in data_lines[:5]:
#     print(line)

all_emails_list = []

for line in data_lines[1:15]:
    all_emails_list.append(line[3])
# print(all_emails_list)

full_name_list = []

for line in data_lines[1:]:
    full_name_list.append(line[1] + " " + line[2])
# print(full_name_list)

# write a CSV file
# csv - comma-separated values: ','
# tsv - tab-separated values: '\'

csv_file_out = open("csv_save.csv", mode = 'w', newline = '')
csv_writer = csv.writer(csv_file_out, delimiter = ',')
csv_writer.writerow(['a', 'b', 'c'])
csv_writer.writerows([[1,2,3], [4,5,6]])

csv_file_out.close()

# append
f_csv = open('csv_save.csv', mode='a', newline='')
csv_writer = csv.writer(f_csv, delimiter = ',')
csv_writer.writerow(['1', '2', '3'])