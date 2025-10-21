from nhansu import NhanVien, HanhChinh, TiepThi, TruongPhong
from quanlyfile import QuanLyTxt, QuanLyCsv, QuanLyJson, QuanLyXml, CLASS_MAP

"""Module này chứa lớp QuanLyNhanSu để quản lý các hoạt động trong chương trình quản lý nhân sự."""

class QuanLyNhanSu:
    """
    Lớp quản lý các hoạt động liên quan đến nhân sự:
    - Thêm, xóa, sửa, tìm kiếm nhân viên.
    - Sắp xếp.
    """
    def __init__(self):
        self._file_name_base = "data_nhansu"
        self._current_file_type = ".txt"
        # Dictionary chứa các đối tượng handler, sẵn sàng để sử dụng
        self._handlers = {
            ".txt": QuanLyTxt(),
            ".csv": QuanLyCsv(),
            ".json": QuanLyJson(),
            ".xml": QuanLyXml()
        }
        self._nv_moi = None  # Biến tạm để giữ nhân viên mới trước khi lưu
        self._danh_sach_nv = []  # Danh sách nhân viên hiện tại

    # --- Phần tương tác với File Handlers ---
    def set_file_type(self):
        """Cho phép người dùng chọn định dạng file để làm việc."""
        print("Chọn định dạng file:")
        types = list(self._handlers.keys())
        for i, ftype in enumerate(types):
            print(f"{i+1}. {ftype}")
        try:
            choice = int(input("Lựa chọn của bạn: ")) - 1
            if 0 <= choice < len(types):
                self._current_file_type = types[choice]
                print(f"Đã chuyển sang làm việc với file *{self._current_file_type}")
                self.doc_file() # Đọc lại dữ liệu từ file có định dạng mới
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Vui lòng nhập một số.")

    def luu_file(self, data: list[HanhChinh | TiepThi | TruongPhong | list] ):
        """Ủy quyền việc ghi file cho handler hiện tại."""
        file_path = self._file_name_base + self._current_file_type
        handler = self._handlers[self._current_file_type]
        handler.write(file_path, data)

        print(f"Đã lưu thành công vào file '{file_path}'.")

    def doc_file(self):
        """Ủy quyền việc đọc file cho handler hiện tại."""
        file_path = self._file_name_base + self._current_file_type
        handler = self._handlers[self._current_file_type]
        self._danh_sach_nv = handler.read(file_path)
        print(f"Đã tải {len(self._danh_sach_nv)} nhân viên từ file '{file_path}'.")

    def tao_ma_nv(self, chuc_vu_class_name: str) -> str:
        """Tạo mã nhân viên tự động theo prefix và số thứ tự."""
        prefix_map = {"HanhChinh": "HC", "TiepThi": "TT", "TruongPhong": "TP"}
        prefix = prefix_map.get(chuc_vu_class_name, "XX")
        max_id = 0
        for nv in self._danh_sach_nv:
            if nv.ma_nv and nv.ma_nv.startswith(prefix):
                try: max_id = max(max_id, int(nv.ma_nv[len(prefix):]))
                except ValueError: continue
        return f"{prefix}{max_id + 1:04d}"

    def them_nhan_vien(self) -> None:
        """Y1: Thêm nhân viên mới và lưu vào file."""
        self._nv_moi = self._nhap_thong_tin_nv_moi()
        if not self._nv_moi:
            return
        
        self.luu_file(self._nv_moi)
        self._nv_moi = None  # Reset sau khi lưu
        self.doc_file()
        print("Đã thêm nhân viên thành công và cập nhật file.")

    def _nhap_thong_tin_nv_moi(self):
        """
        Hàm phụ trợ để lấy thông tin nhân viên mới từ người dùng.
        - Gồm loại nhận viên, họ tên, lương và các thông tin khác nếu có.
        - Gọi hàm tạo mã nhân viên.
        """
        print("Chọn loại nhân viên để thêm:")
        for i, cls_name in enumerate(CLASS_MAP.keys(), 1):
            print(f"{i}. {cls_name}")
        loai_nv = int(input("Chọn loại nhân viên: "))
        
        if loai_nv == 1: nv, cls_name = HanhChinh(), "HanhChinh"
        elif loai_nv == 2: nv, cls_name = TiepThi(), "TiepThi"
        elif loai_nv == 3: nv, cls_name = TruongPhong(), "TruongPhong"
        else: print("Lựa chọn không hợp lệ."); return None
        
        nv.ma_nv = self.tao_ma_nv(cls_name)
        nv.ho_ten = input("Nhập họ tên: ")
        nv.luong = float(input("Nhập lương cơ bản: "))
        
        if isinstance(nv, TiepThi):
            nv.doanh_so = float(input("Nhập doanh số: "))
            nv.hoa_hong = float(input("Nhập tỉ lệ hoa hồng (vd: 0.1): "))
        elif isinstance(nv, TruongPhong):
            nv.luong_trach_nhiem = float(input("Nhập lương trách nhiệm: "))
        return nv
    
    def _xuat_danh_sach(self, danh_sach: list) -> None:
        """Y2: Xuất danh sách nhân viên ra màn hình."""
        if not danh_sach:
            print("Danh sách nhân viên trống.")
            return
        print(f"\n--- Danh sách nhân viên ({len(danh_sach)} nhân viên) ---")
        print(f"{'Mã NV':<6}| {'Họ Tên':<30}| {'Chức Vụ':<13}| {'Lương':<16}| {'Doanh số':<16}| {'Hoa hồng':<10}| {'Lương trách nhiệm':<18}| {'Thu Nhập':<16}| {'Thuế TN':<16}")
        for nv in danh_sach:
            nv.xuat_thong_tin()
    
    def xuat_danh_sach_all(self) ->None:
        """Xuất toàn bộ danh sách nhân viên."""
        self._xuat_danh_sach(self._danh_sach_nv)

    def _is_valid_ma_nv(self, ma_nv: str) -> bool:
        """Kiểm tra định dạng mã nhân viên."""
        if not ma_nv or len(ma_nv) != 6:
            return False
        prefix = ma_nv[:2].upper()
        return prefix in {"HC", "TT", "TP"} and ma_nv[2:].isdigit()

    def tim_nhan_vien_theo_ma(self, search_ma_nv: str) -> NhanVien | None:
        """Y3: Tìm nhân viên theo mã."""
        if self._is_valid_ma_nv(search_ma_nv) == False:
            print("Mã nhân viên không hợp lệ. Mã Phải bắt đầu bằng HC, TT, TP và theo sau là 4 chữ số.")
            return None
        for nv in self._danh_sach_nv:
            if nv.ma_nv == search_ma_nv.upper():
                return nv
        return None

    def xoa_nhan_vien_theo_ma(self, search_ma_nv: str) -> None:
        """Y4: Xóa nhân viên và cập nhật file."""
        nv = self.tim_nhan_vien_theo_ma(search_ma_nv)
        if nv:
            nv.xuat_thong_tin()
            confirm = input(f"Bạn có chắc chắn muốn xóa nhân viên {nv.ma_nv}? (y/n): ").strip().lower()
            if confirm == 'y':
                self._danh_sach_nv.remove(nv)
                print(f"Đã xóa nhân viên: {nv.ho_ten}")
                self.luu_file(self._danh_sach_nv)
                print("Đã xóa và cập nhật file.")
        else:
            print("Không tìm thấy nhân viên.")

    def cap_nhat_thong_tin(self) -> None:
        """Y5: Cập nhật thông tin nhân viên và lưu file."""
        ma_nv = input("Nhập mã nhân viên cần cập nhật: ").strip()
        nv = self.tim_nhan_vien_theo_ma(ma_nv)

        if not nv:
            print("Không tìm thấy nhân viên cần cập nhật.")
            return
        
        print("Thông tin hiện tại của nhân viên:")
        nv.xuat_thong_tin()
        print("Thông tin bạn muốn cập nhật (Không thể cập nhật mã nhân viên) bỏ trống (enter) nếu bạn muốn giữa nguyên:")
        if isinstance(nv, TiepThi):
            if (new_ho_ten := input(f"Họ tên ({nv.ho_ten}): ")) != "":
                nv.ho_ten = new_ho_ten
            if (new_luong := input(f"Lương cơ bản ({nv.luong}): ")) != "":
                nv.luong = new_luong
            if (new_doanh_so := input(f"Doanh số ({nv.doanh_so}): ")) != "":
                nv.doanh_so = new_doanh_so
            if (new_hoa_hong := input(f"Tỉ lệ hoa hồng ({nv.hoa_hong}): ")) != "":
                nv.hoa_hong = new_hoa_hong
        elif isinstance(nv, TruongPhong):
            if (new_ho_ten := input(f"Họ tên ({nv.ho_ten}): ")) != "":
                nv.ho_ten = new_ho_ten
            if (new_luong := input(f"Lương cơ bản ({nv.luong}): ")) != "":
                nv.luong = new_luong
            if (new_luong_trach_nhiem := input(f"Lương trách nhiệm ({nv.luong_trach_nhiem}): ")) != "":
                nv.luong_trach_nhiem = new_luong_trach_nhiem
        else:
            if (new_ho_ten := input(f"Họ tên ({nv.ho_ten}): ")) != "":
                nv.ho_ten = new_ho_ten
            if (new_luong := input(f"Lương cơ bản ({nv.luong}): ")) != "":
                nv.luong = new_luong

        self.luu_file(self._danh_sach_nv)
        print("Đã cập nhật và lưu file.")

    def tim_theo_khoang_luong(self):
        """Y6: Tìm nhân viên theo khoảng lương."""
        try: 
            min_luong = float(input("Nhập mức lượng thấp nhất: "))
            max_luong = float(input("Nhập mức lương cao nhất: "))
            if min_luong > max_luong:
                print("Mức lương thấp nhất phải nhỏ hơn mức lương cao nhất.")
                return
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")
            return
        nv_trong_khoang_luong = [nv for nv in self._danh_sach_nv if min_luong <= nv.luong <= max_luong]
        if not nv_trong_khoang_luong:
            print(f"Không có nhân viên nào trong khoảng lương {min_luong:,} - {max_luong:,}")
            return
        self._xuat_danh_sach(nv_trong_khoang_luong)

    def sap_xep_theo_ten(self):
        """Y7: Sắp xếp nhân viên theo họ và tên."""
        # Sử dụng lambda để sắp xếp theo thuộc tính ho_ten
        self._danh_sach_nv.sort(key=lambda nv: nv.ho_ten)
        print("Đã sắp xếp danh sách theo tên.")
        self._xuat_danh_sach(self._danh_sach_nv)

    def sap_xep_theo_thu_nhap(self):
        """Y8: Sắp xếp nhân viên theo thu nhập giảm dần."""
        # Sử dụng lambda để sắp xếp dựa trên kết quả của phương thức get_thu_nhap()
        self._danh_sach_nv.sort(key=lambda nv: nv.thu_nhap, reverse=True)
        print("Đã sắp xếp danh sách theo thu nhập giảm dần.")
        self._xuat_danh_sach(self._danh_sach_nv)

    def top_5_thu_nhap_cao(self):
        """Y9: Xuất 5 nhân viên có thu nhập cao nhất."""
        # Sắp xếp và lấy 5 phần tử đầu tiên
        sorted_list = sorted(self._danh_sach_nv, key=lambda nv: nv.thu_nhap, reverse=True)
        top_5 = sorted_list[:5]
        print("Top 5 nhân viên có thu nhập cao nhất:")
        self._xuat_danh_sach(top_5)


