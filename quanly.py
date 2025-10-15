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
        self.doc_file() # Tải dữ liệu ban đầu khi khởi tạo

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

    def luu_file(self):
        """Ủy quyền việc ghi file cho handler hiện tại."""
        file_path = self._file_name_base + self._current_file_type
        handler = self._handlers[self._current_file_type]
        handler.write(file_path, self._nv_moi)
        print(f"Đã lưu thành công vào file '{file_path}'.")

    def doc_file(self):
        """Ủy quyền việc đọc file cho handler hiện tại."""
        file_path = self._file_name_base + self._current_file_type
        handler = self._handlers[self._current_file_type]
        self._danh_sach_hien_co = handler.read(file_path)
        print(f"Đã tải {len(self._danh_sach_hien_co)} nhân viên từ file '{file_path}'.")

    def tao_ma_nv(self, chuc_vu_class_name: str) -> str:
        """Tạo mã nhân viên tự động theo prefix và số thứ tự."""
        prefix_map = {"HanhChinh": "HC", "TiepThi": "TT", "TruongPhong": "TP"}
        prefix = prefix_map.get(chuc_vu_class_name, "XX")
        max_id = 0
        for nv in self._danh_sach_hien_co:
            if nv.ma_nv and nv.ma_nv.startswith(prefix):
                try: max_id = max(max_id, int(nv.ma_nv[len(prefix):]))
                except ValueError: continue
        return f"{prefix}{max_id + 1:04d}"

    def them_nhan_vien(self) -> None:
        """Y1: Thêm nhân viên mới và lưu vào file."""
        self._nv_moi = self._nhap_thong_tin_nv_moi()
        if not self._nv_moi:
            return
        
        self.luu_file()
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
    
    def xuat_danh_sach(self) -> None:
        """Y2: Xuất danh sách nhân viên ra màn hình."""
        if not self._danh_sach_hien_co:
            print("Danh sách nhân viên trống.")
            return
        print(f"\n--- Danh sách nhân viên ({len(self._danh_sach_hien_co)} nhân viên) ---")
        print(f"{'Mã NV':<6}| {'Họ Tên':<30}| {'Chức Vụ':<13}| {'Lương':<16}| {'Doanh số':<16}| {'Hoa hồng':<10}| {'Lương trách nhiệm':<18}| {'Thu Nhập':<16}| {'Thuế TN':<16}")
        for nv in self._danh_sach_hien_co:
            nv.xuat_thong_tin()

    def tim_nhan_vien_theo_ma(self, search_ma_nv: str) -> NhanVien | None:
        """Y3: Tìm nhân viên theo mã."""
        for nv in self._danh_sach_hien_co:
            if nv.ma_nv == search_ma_nv:
                return nv
        return None

    def xoa_nhan_vien_theo_ma(self, search_ma_nv: str) -> None:
        """Y4: Xóa nhân viên và cập nhật file."""
        nv = self.tim_nhan_vien_theo_ma(search_ma_nv)
        if nv:
            self._danh_sach_hien_co.remove(nv)
            print(f"Đã xóa nhân viên: {nv.ho_ten}")
        else:
            print("Không tìm thấy nhân viên.")

        self.luu_file()
        print("Đã xóa và cập nhật file.")

    def cap_nhat_thong_tin(self):
        """Y5: Cập nhật thông tin nhân viên và lưu file."""
        # ... (Nhập mã, tìm, cho phép sửa thông tin)
        self.luu_file()
        print("Đã cập nhật và lưu file.")

    def tim_theo_khoang_luong(self):
        """Y6: Tìm nhân viên theo khoảng lương."""
        # ...
        pass
        
    def sap_xep_theo_ten(self):
        """Y7: Sắp xếp nhân viên theo họ và tên."""
        # Sử dụng lambda để sắp xếp theo thuộc tính ho_ten
        self._danh_sach_hien_co.sort(key=lambda nv: nv.ho_ten)
        print("Đã sắp xếp danh sách theo tên.")
        self.xuat_danh_sach()

    def sap_xep_theo_thu_nhap(self):
        """Y8: Sắp xếp nhân viên theo thu nhập giảm dần."""
        # Sử dụng lambda để sắp xếp dựa trên kết quả của phương thức get_thu_nhap()
        self._danh_sach_hien_co.sort(key=lambda nv: nv.get_thu_nhap(), reverse=True)
        print("Đã sắp xếp danh sách theo thu nhập giảm dần.")
        self.xuat_danh_sach()

    def top_5_thu_nhap_cao(self):
        """Y9: Xuất 5 nhân viên có thu nhập cao nhất."""
        # Sắp xếp và lấy 5 phần tử đầu tiên
        sorted_list = sorted(self._danh_sach_hien_co, key=lambda nv: nv.get_thu_nhap(), reverse=True)
        top_5 = sorted_list[:5]
        print("Top 5 nhân viên có thu nhập cao nhất:")
        for nv in top_5:
            nv.xuat_thong_tin()


