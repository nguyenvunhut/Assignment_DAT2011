import csv

# Đường dẫn tới file txt gốc và file csv đích
input_file = 'data_nhansu.txt'
output_file = 'data_nhansu.csv'

# Đọc dữ liệu từ file txt và ghi sang file csv
with open(input_file, 'r', encoding='utf-8') as txt_file:
    lines = txt_file.readlines()

with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    for line in lines:
        row = line.strip().split(',')
        writer.writerow(row)

print(f"Đã chuyển dữ liệu từ {input_file} sang {output_file} thành công.")
