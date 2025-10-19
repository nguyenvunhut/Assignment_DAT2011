
<<<<<<< HEAD
handler = QuanLyTxt()
data = handler.read("data_nhansu.txt")
if not data:
    print("Không có dữ liệu trong file.")
for nv in data:
    nv.xuat_thong_tin()
=======
ma_nv = input("Nhập mã nhân viên cần tìm: ").strip().upper()

def is_valid_ma_nv(ma_nv):
    if not ma_nv or len(ma_nv) != 6:
        return False
    prefix = ma_nv[:2].upper()
    return prefix in {"HC", "TT", "TP"} and ma_nv[2:].isdigit()

print(ma_nv)
print(ma_nv[:2])
print(ma_nv[2:])
print(is_valid_ma_nv(ma_nv))
>>>>>>> 9f4aded0f5d0e2d4925c73b6e7151779f0f6e36e
