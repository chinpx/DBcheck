import pandas as pd
import csv
import re
import os


input_directory = r"./input"
temp_directory = r"./temp"
output_directory = r"./output"

def process_txt_file(input_path, output_path, separator=','):
    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        current_line = ""
        for line in input_file:
            # Loại bỏ ký tự NULL
            line = line.replace('\x00', '')
            # Kiểm tra nếu dòng bắt đầu bằng ký tự '/'
            if line.startswith('/'):
                # Nếu có một dòng hiện tại, lưu nó trước khi bắt đầu một dòng mới
                if current_line:
                    # Loại bỏ khoảng trắng thừa xung quanh dấu phẩy
                    current_line = re.sub(r'\s*,\s*', ',', current_line.strip())
                    # Thay thế các khoảng trắng liên tiếp bằng dấu phẩy hoặc dấu cách
                    cleaned_line = re.sub(r'\s+', separator, current_line)
                    # ghi dòng hiện tại (sau khi làm sạch) vào file
                    output_file.write(cleaned_line + '\n')
                # Bắt đầu một dòng mới
                current_line = line.strip()
            else:
                # Nếu không, nối dòng hiện tại với dòng trước đó
                current_line += " " + line.strip()

        # Đừng quên lưu dòng cuối cùng
        if current_line:
            # Loại bỏ khoảng trắng thừa xung quanh dấu phẩy
            current_line = re.sub(r'\s*,\s*', ',', current_line.strip())
            # Thay thế các khoảng trắng liên tiếp bằng dấu phẩy hoặc dấu cách
            cleaned_line = re.sub(r'\s+', separator, current_line)
            output_file.write(cleaned_line + '\n')

def process_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not os.path.exists(input_directory):
        os.makedirs(input_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):  # Chỉ xử lý các tệp .txt
            input_file_path = os.path.join(input_directory, filename)
            output_file_name = os.path.splitext(filename)[0] + '.csv'
            output_file_path = os.path.join(output_directory, output_file_name)
            process_txt_file(input_file_path, output_file_path)

# Đọc file CSV và chuẩn hóa số lượng cột
# Đọc file CSV và tìm số dòng tối đa và cột tối đa
#
def normalize_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    max_columns = max(len(row) for row in rows)
    normalized_rows = [row + [''] * (max_columns - len(row)) for row in rows]

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(normalized_rows)

# Convert txt to CSV đẩy vào thư mục temp
process_directory(input_directory, temp_directory)


