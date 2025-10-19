import os
from abc import ABC, abstractmethod
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import data_nhansu
from nhansu import HanhChinh, TiepThi, TruongPhong

# Utility: Ánh xạ chuỗi chức vụ với Lớp tương ứng để tái tạo đối tượng
CLASS_MAP = {
    "Hành Chính": HanhChinh,
    "Tiếp Thị": TiepThi,
    "Trưởng Phòng": TruongPhong
}

class FileHandler(ABC):
    """Lớp cơ sở trừu tượng định nghĩa 'khung' cho các lớp xử lý file."""
    @abstractmethod
    def read(self, file_path: str) -> list:
        pass
    @abstractmethod
    def write(self, file_path: str, data: list[HanhChinh | TiepThi | TruongPhong]) -> None:
        pass

class QuanLyTxt(FileHandler):
    """
    Xử lý việc đọc/ghi file định dạng .txt.\n
    File lưu theo kiểu: ma_nv, ho_ten, chuc_vu, luong, thong_tin_them1, thong_tin_them2\n
    Ví dụ:\n
    ma_nv, ho_ten, chuc_vu, luong, thong_tin_them1, thong_tin_them2\n
    HC0001,Nguyen Van A,Hành Chính,50000000\n
    TT0002,Le Thi B,Tiếp Thị,30000000,200000000,0.05\n
    TP0003,Tran Van C,Trưởng Phòng,70000000,150000\n
    """

    def read(self, file_path: str) -> list:
        danh_sach = []

        if not os.path.exists(file_path): # kiểm tra file tồn tại
            print(f"File '{file_path}' không tồn tại.")
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue # bỏ qua dòng trống

                parts = line.split(',')
                if len(parts) < 4:
                    continue  # bỏ qua dòng sai định dạng

                ma_nv, ho_ten, chuc_vu, luong = parts[:4]
                NhanVienClass = CLASS_MAP.get(chuc_vu)
                if not NhanVienClass:
                    continue

                nv = NhanVienClass()
                nv.ma_nv = ma_nv
                nv.ho_ten = ho_ten
                nv.luong = float(luong)

                # Nếu là nhân viên đặc biệt có thêm thông tin
                if isinstance(nv, TiepThi):
                    nv.doanh_so = float(parts[4])
                    nv.hoa_hong = float(parts[5])
                elif isinstance(nv, TruongPhong):
                    nv.luong_trach_nhiem = float(parts[6])

                danh_sach.append(nv)

        return danh_sach

    # write method chia ra làm 2 phần, ghi dữ liệu nhân viên mới và cập nhật lại danh sách gồm (thay đổi, xóa nhân viên)
    def write(self, file_path: str, nv_moi) -> None:
        """
        Ghi dữ liệu ra file với các cột cố định.
        Mở file ở chế độ 'a' (append) để ghi thêm dữ liệu mà không làm mất dữ liệu cũ
        """
        # Định nghĩa tiêu đề cho các cột
        headers = [
            'Mã NV', 'Họ Tên', 'Chức Vụ', 'Lương', 'Doanh số', 
            'Hoa hồng', 'Lương trách nhiệm', 'Thu Nhập', 'Thuế TN'
        ]
        
        # Nếu nv_moi là một đối tượng nhân viên với thì mở file ở chế độ 'a'
        # Nếu là một danh sách thì mở file ở chế độ 'w' để ghi đè
        if isinstance(nv_moi, list):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                # Ghi dòng tiêu đề
                f.write(','.join(headers) + '\n')
                for nv in nv_moi:
                    # Chuẩn bị các giá trị mặc định cho các cột có thể trống
                    doanh_so = 0.0
                    hoa_hong = 0.0
                    luong_trach_nhiem = 0.0

                    chuc_vu = nv.chuc_vu

                    # Cập nhật giá trị riêng tùy theo loại nhân viên
                    if isinstance(nv, TiepThi):
                        doanh_so = nv.doanh_so
                        hoa_hong = nv.hoa_hong
                    elif isinstance(nv, TruongPhong):
                        luong_trach_nhiem = nv.luong_trach_nhiem
                    
                    # Tạo một hàng dữ liệu theo đúng thứ tự của tiêu đề
                    row = [
                        nv.ma_nv,
                        nv.ho_ten,
                        chuc_vu,
                        nv.luong,
                        doanh_so,
                        hoa_hong,
                        luong_trach_nhiem,
                        nv.thu_nhap,
                        nv.thue_thu_nhap
                    ]
                    f.write(','.join(map(str, row)) + '\n')
        elif isinstance(nv_moi, (HanhChinh, TiepThi, TruongPhong)):
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                # Ghi dòng tiêu đề nếu file mới hoặc trống
                if os.path.getsize(file_path) == 0:
                    f.write(','.join(headers) + '\n')
                
                # Chuẩn bị các giá trị mặc định cho các cột có thể trống
                doanh_so = 0.0
                hoa_hong = 0.0
                luong_trach_nhiem = 0.0

                chuc_vu = nv_moi.chuc_vu

                # Cập nhật giá trị riêng tùy theo loại nhân viên
                if isinstance(nv_moi, TiepThi):
                    doanh_so = nv_moi.doanh_so
                    hoa_hong = nv_moi.hoa_hong
                elif isinstance(nv_moi, TruongPhong):
                    luong_trach_nhiem = nv_moi.luong_trach_nhiem
                
                # Tạo một hàng dữ liệu theo đúng thứ tự của tiêu đề
                row = [
                    nv_moi.ma_nv,
                    nv_moi.ho_ten,
                    chuc_vu,
                    nv_moi.luong,
                    doanh_so,
                    hoa_hong,
                    luong_trach_nhiem,
                    nv_moi.thu_nhap,
                    nv_moi.thue_thu_nhap
                ]
                f.write(','.join(map(str, row)) + '\n')
        else:
            raise ValueError("Dữ liệu không hợp lệ. Phải là đối tượng nhân viên hoặc danh sách nhân viên.")


class QuanLyCsv(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .csv."""
    # ... code
    def __init__(self):
        super().__init__()

    def read(self, file_path):
        return super().read(file_path)
    
    def write(self, file_path, data):
        return super().write(file_path, data)

class QuanLyJson(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .json."""
    # ... code
    def __init__(self):
        super().__init__()

    def read(self, file_path):
        return super().read(file_path)
    
    def write(self, file_path, data):
        return super().write(file_path, data)

class QuanLyXml(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .xml."""
    # ... code
    def __init__(self):
        super().__init__() 
    def read(self, file_path):
        danh_sach = []

        if not os.path.exists(file_path):
            print(f"File '{file_path}' không tồn tại.")
            return []
        try:
            tree = ET.parse(file_path)
            for nv_element in tree.findall('NHAN_VIEN'): 
                nv_data = {}
                for child in nv_element:
                    tag_name = child.tag 
                    value = child.text.strip() if child.text else ''
                    try:
                        nv_data[tag_name] = float(value)
                    except ValueError:
                        nv_data[tag_name] = value

                if nv_data:
                    danh_sach.append(nv_data)
                
        except ET.ParseError as e:
            print(f"Lỗi khi phân tích file XML '{file_path}': {e}")
        return super().read(file_path)
    
    def write(self, file_path, data):
        root = ET.Element('DANHSACH_NHANSU')      
        for nv_moi in  data_nhansu:
            nv_element = ET.SubElement(root, 'NHAN_VIEN')
            
            for key, value in nv_moi.items():
                if value is not None and value != '':
                    ET.SubElement(nv_element, key).text = str(value)
                
        tree = ET.ElementTree(root)
        try:
            ET.indent(tree, space="  ", level=0) 
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            print(f"Đã ghi thành công {len(data_nhansu)} nhân viên vào file: {file_path}")
        except Exception as e:
            print(f"Lỗi khi ghi file XML '{file_path}': {e}")
        return super().write(file_path, data)
