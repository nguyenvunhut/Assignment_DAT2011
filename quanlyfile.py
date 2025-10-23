import os
from abc import ABC, abstractmethod
import csv
import json
import xml.etree.ElementTree as ETree
from xml.dom import minidom
from typing import TypeVar, Union
from nhansu import HanhChinh, TiepThi, TruongPhong
EmployeeType = TypeVar('EmployeeType', HanhChinh, TiepThi, TruongPhong)

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
    
    def read(self, file_path: str) -> list:
        danh_sach = []
        
        if not os.path.exists(file_path):
            print(f"File '{file_path}' không tồn tại.")
            return danh_sach
            
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    chuc_vu = row['Chức Vụ']
                    NhanVienClass = CLASS_MAP.get(chuc_vu)
                    
                    if not NhanVienClass:
                        continue
                    
                    nv = NhanVienClass()
                    nv.ma_nv = row['Mã NV']
                    nv.ho_ten = row['Họ Tên']
                    nv.luong = float(row['Lương'])
                    
                    if isinstance(nv, TiepThi):
                        nv.doanh_so = float(row['Doanh số'])
                        nv.hoa_hong = float(row['Hoa hồng'])
                    elif isinstance(nv, TruongPhong):
                        nv.luong_trach_nhiem = float(row['Lương trách nhiệm'])
                    
                    danh_sach.append(nv)
                    
        except Exception as e:
            print(f"Lỗi khi đọc file CSV '{file_path}': {e}")
            
        return danh_sach

    def write(self, file_path: str, data) -> None:
        headers = [
            'Mã NV', 'Họ Tên', 'Chức Vụ', 'Lương', 'Doanh số', 
            'Hoa hồng', 'Lương trách nhiệm', 'Thu Nhập', 'Thuế TN'
        ]
        
        try:
            if isinstance(data, list):
                # Ghi toàn bộ danh sách
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    
                    for nv in data:
                        row = self._tao_dong_du_lieu(nv)
                        writer.writerow(row)
                        
            elif isinstance(data, (HanhChinh, TiepThi, TruongPhong)):
                # Ghi thêm một nhân viên mới
                file_exists = os.path.exists(file_path)
                
                with open(file_path, 'a', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    
                    if not file_exists or os.path.getsize(file_path) == 0:
                        writer.writeheader()
                    
                    row = self._tao_dong_du_lieu(data)
                    writer.writerow(row)
                    
            else:
                raise ValueError("Dữ liệu không hợp lệ. Phải là đối tượng nhân viên hoặc danh sách nhân viên.")
                
        except Exception as e:
            print(f"Lỗi khi ghi file CSV '{file_path}': {e}")

    def _tao_dong_du_lieu(self, nv):
        """Tạo dictionary chứa dữ liệu của một nhân viên để ghi vào CSV"""
        doanh_so = 0.0
        hoa_hong = 0.0
        luong_trach_nhiem = 0.0

        if isinstance(nv, TiepThi):
            doanh_so = nv.doanh_so
            hoa_hong = nv.hoa_hong
        elif isinstance(nv, TruongPhong):
            luong_trach_nhiem = nv.luong_trach_nhiem

        return {
            'Mã NV': nv.ma_nv,
            'Họ Tên': nv.ho_ten,
            'Chức Vụ': nv.chuc_vu,
            'Lương': nv.luong,
            'Doanh số': doanh_so,
            'Hoa hồng': hoa_hong,
            'Lương trách nhiệm': luong_trach_nhiem,
            'Thu Nhập': nv.thu_nhap,
            'Thuế TN': nv.thue_thu_nhap
        }

class QuanLyJson(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .json."""
    # ... code
    def __init__(self):
        super().__init__()

    def _nv_to_dict(self, nv):
        """Chuẩn hóa object nhân viên về dict để ghi JSON."""
        data = {
            "ma_nv": nv.ma_nv,
            "ho_ten": nv.ho_ten,
            "chuc_vu": getattr(nv, "chuc_vu", ""),
            "luong": nv.luong,
            "doanh_so": 0.0,
            "hoa_hong": 0.0,
            "luong_trach_nhiem": 0.0,
            "thu_nhap": nv.thu_nhap,
            "thue_tn": nv.thue_thu_nhap,
        }
        # Bổ sung theo loại
        if isinstance(nv, TiepThi):
            data["doanh_so"] = nv.doanh_so
            data["hoa_hong"] = nv.hoa_hong
        elif isinstance(nv, TruongPhong):
            data["luong_trach_nhiem"] = nv.luong_trach_nhiem
        return data

    def _dict_to_nv(self, d: dict):
        """Từ 1 dict trong JSON dựng lại đúng class nhân viên."""
        chuc_vu = d.get("chuc_vu", "").strip()
        NhanVienClass = CLASS_MAP.get(chuc_vu)
        if not NhanVienClass:
            return None

        nv = NhanVienClass()
        nv.ma_nv = d.get("ma_nv", "")
        nv.ho_ten = d.get("ho_ten", "")
        nv.luong = d.get("luong", 0.0)

        # Tùy loại mà gán thêm trường
        if isinstance(nv, TiepThi):
            nv.doanh_so = d.get("doanh_so", 0.0)
            nv.hoa_hong = d.get("hoa_hong", 0.0)
        elif isinstance(nv, TruongPhong):
            nv.luong_trach_nhiem = d.get("luong_trach_nhiem", 0.0)

        return nv

    def read(self, file_path: str) -> list:
        if not os.path.exists(file_path):
            print(f"File '{file_path}' chưa tồn tại → trả về list rỗng.")
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError:
            print("File JSON rỗng hoặc sai định dạng → trả về list rỗng.")
            return []
        except Exception as e:
            print(f"Lỗi đọc file JSON: {e}")
            return []

        # Nếu là object bọc list, lấy list đầu tiên bắt gặp
        if isinstance(raw, dict):
            for v in raw.values():
                if isinstance(v, list):
                    raw = v
                    break

        ds = []
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    nv = self._dict_to_nv(item)
                    if nv:
                        ds.append(nv)

        print(f"Đã đọc {len(ds)} nhân viên từ '{file_path}'.")
        return ds
    
    def write(self, file_path: str, data) -> None:
        # Đọc dữ liệu cũ (để hỗ trợ append khi ghi 1 nhân viên)
        old = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    old = json.load(f)
                    if not isinstance(old, list):
                            old = []
            except Exception:
                        old = []

        if isinstance(data, list):
            payload = [self._nv_to_dict(nv) for nv in data]
        elif isinstance(data, (HanhChinh, TiepThi, TruongPhong)):
            payload = old + [self._nv_to_dict(data)]
        else:
            raise ValueError("Dữ liệu ghi JSON phải là list nhân viên hoặc 1 đối tượng nhân viên.")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f" Đã ghi {len(payload)} nhân viên vào '{file_path}'.")

class QuanLyXml(FileHandler):
    """Xử lý việc đọc/ghi file định dạng .xml."""

    def read(self, file_path: str) -> list:
        danh_sach = []
        if not os.path.exists(file_path):
            print(f"File '{file_path}' không tồn tại.")
            return []
            
        try:
            tree = ETree.parse(file_path)
            root = tree.getroot()
        except ETree.ParseError as e:
            print(f"Lỗi khi phân tích file XML '{file_path}': {e}")
            return []
        except Exception as e:
            print(f"Lỗi không xác định khi đọc file XML '{file_path}': {e}")
            return []
            
        for nv_element in root.findall('NHAN_VIEN'):
            nv_data = {}
            for child in nv_element:
                tag_name = child.tag.lower().strip()
                value = child.text.strip() if child.text else ''
                try:
                    nv_data[tag_name] = float(value)
                except ValueError:
                    nv_data[tag_name] = value

            if not nv_data:
                continue

            try:
                chuc_vu = nv_data.get("chuc_vu", "")
                NhanVienClass = CLASS_MAP.get(chuc_vu)
                if not NhanVienClass:
                    print(f"Không tìm thấy lớp cho chức vụ '{chuc_vu}'")
                    continue

                nv = NhanVienClass()
                nv.ma_nv = nv_data.get("ma_nv", "")
                nv.ho_ten = nv_data.get("ho_ten", "")
                nv.luong = nv_data.get("luong", 0.0)
                nv.doanh_so = nv_data.get("doanh_so", 0.0)
                nv.hoa_hong = nv_data.get("hoa_hong", 0.0)
                nv.luong_trach_nhiem = nv_data.get("luong_trach_nhiem", 0.0)

                danh_sach.append(nv)
            except Exception as e:
                print(f"Lỗi khi chuyển XML thành đối tượng: {e} (Dữ liệu: {nv_data})")
                continue
                
        return danh_sach

    def write(self, file_path: str, data: Union[list[EmployeeType], EmployeeType]) -> None:
        """Ghi toàn bộ danh sách nhân viên ra file .xml (ghi đè)."""
        if os.path.exists(file_path) and not isinstance(data, list):
            existing_data = self.read(file_path)
            existing_data.append(data)
            data = existing_data
        
        employees_to_serialize = [data] if not isinstance(data, list) else data
        
        # Chuyển sang dictionary
        nv_data = []
        for nv in employees_to_serialize:
            temp_dict = vars(nv).copy()
            temp_dict['chuc_vu'] = nv.chuc_vu  # đảm bảo có chức vụ
            nv_data.append(temp_dict)
            
        # Ghi XML
        root = ETree.Element('DANHSACH_NHANSU') 
        
        for employee_dict in nv_data:
            nv_element = ETree.SubElement(root, 'NHAN_VIEN')
            for key, value in employee_dict.items():
                if key in ['thu_nhap', 'thue_tn']:  # giữ nguyên các trường hợp này
                            pass
                        # Bỏ qua giá trị None hoặc rỗng
                if value is not None and value != '':
                    ETree.SubElement(nv_element, key).text = str(value)
                                
                xml_string = ETree.tostring(root, encoding='utf-8') 
                pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="    ")
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                        f.write(pretty_xml)
                    print(f"Đã ghi thành công {len(nv_data)} nhân viên vào file: {file_path}")
                except Exception as e:
                    print(f"Lỗi khi ghi file XML '{file_path}': {e}")