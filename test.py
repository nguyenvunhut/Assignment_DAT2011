
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