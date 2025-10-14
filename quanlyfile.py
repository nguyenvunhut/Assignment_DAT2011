import os
from abc import ABC, abstractmethod
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
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
                if isinstance(nv, TiepThi) and len(parts) >= 6:
                    nv.doanh_so = float(parts[4])
                    nv.hoa_hong = float(parts[5])
                elif isinstance(nv, TruongPhong) and len(parts) >= 5:
                    nv.luong_trach_nhiem = float(parts[4])

                danh_sach.append(nv)

        return danh_sach


    def write(self, file_path: str, data: list) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            for nv in data:
                chuc_vu = nv.__class__.__name__
                base_data = [nv.ma_nv, nv.ho_ten, chuc_vu, nv.luong]

                if isinstance(nv, TiepThi):
                    base_data.extend([nv.doanh_so, nv.hoa_hong])
                elif isinstance(nv, TruongPhong):
                    base_data.append(nv.luong_trach_nhiem)

                f.write(','.join(map(str, base_data)) + '\n')

class QuanLyCsv(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .csv."""
    # ... code

class QuanLyJson(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .json."""
    # ... code

class QuanLyXml(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .xml."""
    # ... code
