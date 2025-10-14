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
        self._danh_sach_nv = [] # list chứa các đối tượng nhân viên
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
        handler.write(file_path, self._danh_sach_nv)
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
        # ... (Code để nhập thông tin và gọi hàm tạo mã)
        # ... (Tạo đối tượng NhanVien, TiepThi, hoặc TruongPhong)
        # ... (Thêm vào self.danh_sach_nv)
        self.luu_file()
        print("Đã thêm nhân viên thành công và cập nhật file.")

    def _nhap_thong_tin_nv_moi(self):
        """Hàm phụ trợ để lấy thông tin nhân viên mới từ người dùng."""
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
        if not self._danh_sach_nv:
            print("Danh sách nhân viên trống.")
            return
        for nv in self._danh_sach_nv:
            nv.xuat_thong_tin()

    def tim_nhan_vien_theo_ma(self, search_ma_nv: str) -> NhanVien | None:
        """Y3: Tìm nhân viên theo mã."""
        for nv in self._danh_sach_nv:
            if nv.ma_nv == search_ma_nv:
                return nv
        return None

    def xoa_nhan_vien_theo_ma(self, search_ma_nv: str) -> None:
        """Y4: Xóa nhân viên và cập nhật file."""
        nv = self.tim_nhan_vien_theo_ma(search_ma_nv)
        if nv:
            self._danh_sach_nv.remove(nv)
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
        self.danh_sach_nv.sort(key=lambda nv: nv.ho_ten)
        print("Đã sắp xếp danh sách theo tên.")
        self.xuat_danh_sach()

    def sap_xep_theo_thu_nhap(self):
        """Y8: Sắp xếp nhân viên theo thu nhập giảm dần."""
        # Sử dụng lambda để sắp xếp dựa trên kết quả của phương thức get_thu_nhap()
        self.danh_sach_nv.sort(key=lambda nv: nv.get_thu_nhap(), reverse=True)
        print("Đã sắp xếp danh sách theo thu nhập giảm dần.")
        self.xuat_danh_sach()

    def top_5_thu_nhap_cao(self):
        """Y9: Xuất 5 nhân viên có thu nhập cao nhất."""
        # Sắp xếp và lấy 5 phần tử đầu tiên
        sorted_list = sorted(self.danh_sach_nv, key=lambda nv: nv.get_thu_nhap(), reverse=True)
        top_5 = sorted_list[:5]
        print("Top 5 nhân viên có thu nhập cao nhất:")
        for nv in top_5:
            nv.xuat_thong_tin()

    def luu_file(self, ):
        """Lưu danh sách nhân viên vào file data_nhansu.txt."""
        # ... (Mở file và ghi từng đối tượng nhân viên theo một định dạng, ví dụ CSV)
        # Gợi ý định dạng: chuc_vu,ma_nv,ho_ten,luong,thong_tin_them1,thong_tin_them2
        # Ví dụ:
        # TruongPhong,TP0001,Nguyen Van A,50000000,10000000
        # TiepThi,TT0001,Tran Thi B,10000000,200000000,0.05
        # HanhChinh,NV0001,Le Van C,12000000
        pass

    def doc_file(self):
        """Đọc dữ liệu nhân viên từ file và nạp vào danh sách."""
        # ... (Mở file, đọc từng dòng, tách dữ liệu)
        # ... (Dựa vào cột 'chuc_vu' để quyết định tạo đối tượng NhanVien, TiepThi hay TruongPhong)
        # ... (Thêm đối tượng đã tạo vào self.danh_sach_nv)
        pass
