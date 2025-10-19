import xml.etree.ElementTree as ET

INPUT_FILE = "data_nhansu.txt"
OUTPUT_FILE = "data_nhansu.xml" # Tên file XML đầu ra

def create_xml_standalone(input_filename, output_filename):
    """Đọc dữ liệu từ file text (dạng CSV) và tạo file XML."""
    
    try:
        # 1. Đọc tất cả nội dung file
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("❌ File dữ liệu trống.")
            return

        # 2. Xử lý Header (Tên cột)
        header_raw = lines[0].strip().split(',')
        
        # Chuẩn hóa tên thẻ XML (thay dấu cách bằng gạch dưới, v.v.)
        headers = [h.strip().replace(' ', '_').replace('Mã_NV', 'Ma_NV').replace('Họ_Tên', 'Ho_Ten').replace('Chức_Vụ', 'Chuc_Vu').replace('Lương_trách_nhiệm', 'Luong_trach_nhiem').replace('Thuế_TN', 'Thue_TN') for h in header_raw]
        
        # 3. Khởi tạo phần tử gốc XML
        root = ET.Element('DANHSACH_NHANSU')
        
        # 4. Xử lý từng dòng dữ liệu (bắt đầu từ dòng thứ 2)
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
                
            data_values = line.split(',')
            
            # Tạo phần tử con NHAN_VIEN
            nhan_vien = ET.SubElement(root, 'NHAN_VIEN')
            
            # Gán giá trị vào các thẻ con tương ứng
            for i in range(len(headers)):
                if i < len(data_values): # Đảm bảo không bị lỗi ngoài phạm vi
                    header = headers[i]
                    value = data_values[i].strip()
                    ET.SubElement(nhan_vien, header).text = value
                else:
                    # Trường hợp dòng dữ liệu thiếu cột (giả định gán giá trị rỗng)
                    ET.SubElement(nhan_vien, headers[i]).text = ''

        # 5. Ghi file XML
        tree = ET.ElementTree(root)
        # Ghi file, sử dụng xml_declaration=True để có <?xml version...?> ở đầu
        ET.ElementTree(root).write(output_filename, encoding="utf-8", xml_declaration=True)

        print(f"✅ Đã tạo file XML thành công: {output_filename}")
        print("Bây giờ bạn có thể mở file này để đọc.")

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file đầu vào '{input_filename}'.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")

# Chạy hàm tạo XML
create_xml_standalone(INPUT_FILE, OUTPUT_FILE)