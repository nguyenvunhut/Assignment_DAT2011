from quanlyfile import FileHandler, QuanLyTxt

handler = QuanLyTxt()
data = handler.read("data_nhansu.txt")
if not data:
    print("Không có dữ liệu trong file.")
for nv in data:
    nv.xuat_thong_tin()
