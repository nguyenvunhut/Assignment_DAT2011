"""
Module này định nghĩa các lớp đối tượng cho các loại nhân sự trong công ty.
- Các đối tượng được khởi tạo rỗng và nhận dữ liệu qua setters.
- Sử dụng @property và @setter để quản lý thuộc tính.
"""

class NhanVien:
    """Lớp cơ sở mô tả một nhân viên."""
    def __init__(self):
        # Khởi tạo các thuộc tính "private" để quản lý qua getters/setters
        self._ma_nv = None
        self._ho_ten = None
        self._luong = 0.0

    # --- Getters ---
    @property
    def ma_nv(self) -> str: return self._ma_nv

    @property
    def ho_ten(self) -> str: return self._ho_ten

    @property
    def luong(self) -> float: return self._luong

    @property
    def thu_nhap(self) -> float: 
        """Tính thu nhập của nhân viên. Mặc định là lương.""" 
        return self._luong

    @property
    def thue_thu_nhap(self) -> float:
        """Tính thuế thu nhập dựa trên thu nhập."""
        current_income = self.thu_nhap
        if current_income < 9000000:
            return 0
        elif 9000000 <= current_income <= 15000000:
            return current_income * 0.10
        else:
            return current_income * 0.12

    # --- Setters ---
    @ma_nv.setter
    def ma_nv(self, value: str) -> None:
        self._ma_nv = value

    @ho_ten.setter
    def ho_ten(self, value: str) -> None:
        # Tên không được để trống
        if not value.strip():
            print("Lỗi: Tên không được để trống.")
        else:
            self._ho_ten = value

    @luong.setter
    def luong(self, value: float) -> None:
        try:
            self._luong = float(value)
        except (ValueError, TypeError):
            print(f"Lỗi: Lương '{value}' không hợp lệ. Đặt lương về 0.")
            self._luong = 0.0
    
    # --- Class Methods ---
    def xuat_thong_tin(self) -> None:
        """Xuất thông tin chi tiết của nhân viên."""
        print(f"Mã NV: {self.ma_nv}, Tên: {self.ho_ten}, Lương: {self.luong:,.0f} VNĐ")
        print(f"  -> Thu nhập: {self.thu_nhap:,.0f} VNĐ, Thuế: {self.thue_thu_nhap:,.0f} VNĐ")


class HanhChinh(NhanVien):
    """Lớp mô tả nhân viên hành chính."""
    def __init__(self):
        super().__init__()
    # Lớp này kế thừa toàn bộ thuộc tính và phương thức của NhanVien
    # không cần thay đổi gì thêm.


class TiepThi(NhanVien):
    """Lớp mô tả nhân viên tiếp thị."""
    def __init__(self):
        super().__init__()
        self._doanh_so = 0.0
        self._hoa_hong = 0.0

    # --- Getters for TiepThi ---
    @property
    def doanh_so(self) -> float:
        return self._doanh_so

    @property
    def hoa_hong(self) -> float:
        return self._hoa_hong
        
    # --- Ghi đè (Override) Getter thu_nhap ---
    @property
    def thu_nhap(self) -> float:
        """Ghi đè phương thức tính thu nhập cho nhân viên tiếp thị."""
        return self._luong + (self._doanh_so * self._hoa_hong)

    # --- Setters for TiepThi ---
    @doanh_so.setter
    def doanh_so(self, value: float) -> None:
        try:
            self._doanh_so = float(value)
        except (ValueError, TypeError):
            print(f"Lỗi: Doanh số '{value}' không hợp lệ. Đặt doanh số về 0.")
            self._doanh_so = 0.0

    @hoa_hong.setter
    def hoa_hong(self, value: float) -> None:
        try:
            # Tỉ lệ hoa hồng, ví dụ: 0.1 cho 10%
            self._hoa_hong = float(value)
        except (ValueError, TypeError):
            print(f"Lỗi: Tỷ lệ hoa hồng '{value}' không hợp lệ. Đặt về 0.")
            self._hoa_hong = 0.0

    # --- Ghi đè (Override) phương thức xuat_thong_tin ---
    def xuat_thong_tin(self):
        """Ghi đè phương thức xuất thông tin để thêm chi tiết của nhân viên tiếp thị."""
        super().xuat_thong_tin()
        # Hiển thị thêm doanh số và hoa hồng
        print(f"  -> Doanh số: {self.doanh_so:,.0f} VNĐ, Hoa hồng: {self.hoa_hong*100:.2f}%")


class TruongPhong(NhanVien):
    """Lớp mô tả trưởng phòng."""
    def __init__(self):
        super().__init__()
        self._luong_trach_nhiem = 0.0

    # --- Getter for TruongPhong ---
    @property
    def luong_trach_nhiem(self) -> float:
        return self._luong_trach_nhiem
    
    # --- Ghi đè (Override) Getter thu_nhap ---
    @property
    def thu_nhap(self) -> float:
        """Ghi đè phương thức tính thu nhập cho trưởng phòng."""
        return self._luong + self._luong_trach_nhiem

    # --- Setter for TruongPhong ---
    @luong_trach_nhiem.setter
    def luong_trach_nhiem(self, value: float) -> None:
        try:
            self._luong_trach_nhiem = float(value)
        except (ValueError, TypeError):
            print(f"Lỗi: Lương trách nhiệm '{value}' không hợp lệ. Đặt về 0.")
            self._luong_trach_nhiem = 0.0

    # --- Ghi đè (Override) phương thức xuat_thong_tin ---
    def xuat_thong_tin(self):
        """Ghi đè phương thức xuất thông tin để thêm chi tiết của trưởng phòng."""
        super().xuat_thong_tin()
        # Hiển thị thêm lương trách nhiệm
        print(f"  -> Lương trách nhiệm: {self.luong_trach_nhiem:,.0f} VNĐ")
