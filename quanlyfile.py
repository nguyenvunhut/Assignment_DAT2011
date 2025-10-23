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

    def _append_nv_to_root(self, root_elem, nv):
        """
        Hàm trợ giúp: Tạo một nhánh <NhanVien> và thêm nó vào root.
        Hàm này cũng thêm tất cả các thuộc tính của nhân viên làm thẻ con.
        """
        nv_elem = ETree.SubElement(root_elem, "NhanVien")
        
        # Hàm nội tuyến (inner function) để tạo thẻ con và gán text
        def create_sub(tag, text_val):
            sub = ETree.SubElement(nv_elem, tag)
            sub.text = str(text_val)

        # Các trường chung
        create_sub("MaNV", nv.ma_nv)
        create_sub("HoTen", nv.ho_ten)
        create_sub("ChucVu", nv.chuc_vu)
        create_sub("Luong", nv.luong)

        # Lấy các trường riêng, đặt mặc định 0.0 nếu không tồn tại
        doanh_so = 0.0
        hoa_hong = 0.0
        luong_trach_nhiem = 0.0

        if isinstance(nv, TiepThi):
            doanh_so = nv.doanh_so
            hoa_hong = nv.hoa_hong
        elif isinstance(nv, TruongPhong):
            luong_trach_nhiem = nv.luong_trach_nhiem

        # Ghi tất cả các trường để file XML đồng nhất
        create_sub("DoanhSo", doanh_so)
        create_sub("HoaHong", hoa_hong)
        create_sub("LuongTrachNhiem", luong_trach_nhiem)
        create_sub("ThuNhap", nv.thu_nhap)
        create_sub("ThueTN", nv.thue_thu_nhap)

    def read(self, file_path: str) -> list:
        danh_sach = []
        if not os.path.exists(file_path):
            print(f"File '{file_path}' không tồn tại.")
            return danh_sach

        try:
            tree = ETree.parse(file_path)
            root = tree.getroot()
        except ETree.ParseError:
            print(f"Lỗi: File XML '{file_path}' rỗng, hỏng hoặc sai định dạng.")
            return danh_sach
        except Exception as e:
            print(f"Lỗi không xác định khi đọc XML: {e}")
            return danh_sach

        # Duyệt qua tất cả các thẻ <NhanVien> con của <DanhSachNhanVien>
        for nv_elem in root.findall('NhanVien'):
            try:
                # Lấy chức vụ để xác định loại Class
                chuc_vu_text = nv_elem.find('ChucVu').text
                NhanVienClass = CLASS_MAP.get(chuc_vu_text)
                
                if not NhanVienClass:
                    print(f"Bỏ qua nhân viên có chức vụ không rõ: {chuc_vu_text}")
                    continue
                
                nv = NhanVienClass()
                nv.ma_nv = nv_elem.find('MaNV').text
                nv.ho_ten = nv_elem.find('HoTen').text
                nv.luong = float(nv_elem.find('Luong').text)
                
                # Gán các trường riêng biệt
                if isinstance(nv, TiepThi):
                    nv.doanh_so = float(nv_elem.find('DoanhSo').text)
                    nv.hoa_hong = float(nv_elem.find('HoaHong').text)
                elif isinstance(nv, TruongPhong):
                    nv.luong_trach_nhiem = float(nv_elem.find('LuongTrachNhiem').text)
                
                danh_sach.append(nv)
                
            except (AttributeError, ValueError, TypeError) as e:
                # AttributeError: nếu .find() trả về None (thiếu thẻ) rồi .text
                # ValueError/TypeError: nếu float() thất bại
                print(f"Bỏ qua một nhân viên trong XML do thiếu dữ liệu hoặc sai định dạng: {e}")
                continue
                
        return danh_sach

    def write(self, file_path: str, data) -> None:
        root = None
        
        if isinstance(data, list):
            # 1. Ghi đè (Overwrite): data là một list
            root = ETree.Element("DanhSachNhanVien")
            for nv in data:
                self._append_nv_to_root(root, nv)
                
        elif isinstance(data, (HanhChinh, TiepThi, TruongPhong)):
            # 2. Ghi thêm (Append): data là một nhân viên
            # Kiểm tra file tồn tại và đọc cấu trúc cũ
            if os.path.exists(file_path):
                try:
                    tree = ETree.parse(file_path)
                    root = tree.getroot()
                except ETree.ParseError:
                    # File tồn tại nhưng rỗng hoặc hỏng, tạo root mới
                    root = ETree.Element("DanhSachNhanVien")
            else:
                # File không tồn tại, tạo root mới
                root = ETree.Element("DanhSachNhanVien")
            
            # Thêm nhân viên mới vào root
            self._append_nv_to_root(root, data)
            
        else:
            raise ValueError("Dữ liệu không hợp lệ. Phải là đối tượng nhân viên hoặc danh sách nhân viên.")

        # Sử dụng minidom để 'pretty print' (format) file XML
        try:
            # Chuyển cây ETree thành chuỗi byte thô
            rough_string = ETree.tostring(root, 'utf-8')
            # Phân tích chuỗi thô bằng minidom
            reparsed = minidom.parseString(rough_string)
            # Tạo chuỗi byte XML đã được format (thụt lề 2 dấu cách)
            pretty_xml_as_bytes = reparsed.toprettyxml(indent="  ", encoding="utf-8")
            
            # Ghi ra file ở chế độ 'wb' (write bytes)
            with open(file_path, "wb") as f:
                f.write(pretty_xml_as_bytes)
                
        except Exception as e:
            print(f"Lỗi khi ghi file XML '{file_path}': {e}")