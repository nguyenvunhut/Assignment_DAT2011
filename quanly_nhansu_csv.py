# ...existing code...
import csv

INPUT_FILE = "data_nhansu.txt"
OUTPUT_FILE = "data_nhansu.csv"  # đổi thành CSV

def create_csv_standalone(input_filename, output_filename):
    """Đọc dữ liệu từ file text (dạng CSV) và tạo file CSV đầu ra (UTF-8 BOM để Excel hiển thị tiếng Việt)."""
    try:
        # 1. Đọc tất cả nội dung file
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print(" File dữ liệu trống.")
            return

        # 2. Xử lý Header (Tên cột)
        header_raw = lines[0].strip().split(',')
        headers = [h.strip().replace(' ', '_').replace('Mã_NV', 'Ma_NV').replace('Họ_Tên', 'Ho_Ten').replace('Chức_Vụ', 'Chuc_Vu').replace('Lương_trách_nhiệm', 'Luong_trach_nhiem').replace('Thuế_TN', 'Thue_TN') for h in header_raw]

        # 3. Xử lý từng dòng dữ liệu (bắt đầu từ dòng thứ 2) và tạo danh sách dict
        rows = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            data_values = [v.strip() for v in line.split(',')]
            # đảm bảo số cột khớp header (nếu thiếu thì điền chuỗi rỗng)
            row = {}
            for i, h in enumerate(headers):
                row[h] = data_values[i] if i < len(data_values) else ''
            rows.append(row)

        if not rows:
            print("Không có dữ liệu để lưu.")
            return

        # 4. Ghi CSV (utf-8-sig để Excel hiển thị tiếng Việt trên Windows)
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Đã tạo file CSV thành công: {output_filename}")

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file đầu vào '{input_filename}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Chạy hàm tạo CSV
create_csv_standalone(INPUT_FILE, OUTPUT_FILE)
# ...existing code...