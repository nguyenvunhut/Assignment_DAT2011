import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data_nhansu.csv"

def is_valid_ma_nv(ma_nv):
    if not ma_nv or len(ma_nv) != 6:
        return False
    prefix = ma_nv[:2].upper()
    return prefix in {"HC", "TT", "TP"} and ma_nv[2:].isdigit()

def try_float(s):
    try:
        return float(s)
    except Exception:
        return None

def check_csv(path):
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except FileNotFoundError:
        print("File không tồn tại:", path)
        return
    except Exception as e:
        print("Lỗi khi đọc CSV:", e)
        return

    print("Headers:", headers)
    print("Số dòng (không tính header):", len(rows))
    # in tối đa 5 dòng mẫu
    for i, r in enumerate(rows[:5], 1):
        print(f"Row {i}:", r)

    # Kiểm tra một số cột số và Ma_NV
    numeric_cols = ["Lương", "Thu_Nhập", "Thue_TN", "Doanh_số", "Hoa_hồng", "Luong_trach_nhiem"]
    conv_errors = []
    invalid_ids = []
    for idx, r in enumerate(rows, 1):
        ma = r.get("Ma_NV", "").strip()
        if not is_valid_ma_nv(ma):
            invalid_ids.append((idx, ma))
        for col in numeric_cols:
            if col in r:
                v = r[col].strip()
                if v == "" or v == "0":
                    continue
                if try_float(v) is None:
                    conv_errors.append((idx, col, v))

    if invalid_ids:
        print("\nMã nhân viên không hợp lệ (hàng, mã):")
        for it in invalid_ids:
            print(it)
    else:
        print("\nTất cả Ma_NV hợp lệ theo quy tắc.")

    if conv_errors:
        print("\nLỗi chuyển số trong các ô (hàng, cột, giá trị):")
        for it in conv_errors[:10]:
            print(it)
    else:
        print("\nKhông tìm thấy lỗi chuyển số đối với các cột kiểm tra.")

if __name__ == "__main__":
    check_csv(CSV_PATH)