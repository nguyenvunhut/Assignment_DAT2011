# yêu cầu của asm
# 1. Nhập danh sách nhân viên từ bàn phím, lưu thông tin vào file
# 2. Đọc thông tin nhân viên từ file và xuất thông tin nhân viên ra màn hình.
# 3. Tìm và hiển thị nhân viên theo mã nhập từ bàn phím
# 4. Xóa nhân viên theo mã nhập từ bàn phím. Cập nhật vào file data
# 5. Cập nhật thông tin nhân viên theo mã nhập từ bàn phím. Cập nhật vào file data
# 6. Tìm các nhân viên theo khoảng lương nhập từ bàn phím.
# 7. Sắp xếp nhân viên theo họ và tên
# 8. Xắp xếp nhân viên theo thu nhập
# 9. Xuất 5 nhân viên có thu nhập cao nhất
TASK = {
    1: "Nhập danh sách nhân viên",
    2: "Xuất danh sách nhân viên", 
    3: "Tìm nhân viên theo mã",
    4: "Xóa nhân viên theo mã",
    5: "Cập nhật thông tin nhân viên",
    6: "Tìm nhân viên theo khoảng lương",
    7: "Sắp xếp nhân viên theo họ tên",
    8: "Sắp xếp nhân viên theo thu nhập",
    9: "Xuất 5 nhân viên có thu nhập cao nhất"
}

def safe_input_int(prompt) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Giá trị nhập vào phải là một số nguyên, vui lòng nhập lại!")

def nhap_nhan_vien():
    print("Chức năng: Nhập danh sách nhân viên")

def xuat_danh_sach():
    print("Chức năng: Xuất danh sách nhân viên")

def tim_theo_ma():
    print("Chức năng: Tìm nhân viên theo mã")

def xoa_theo_ma():
    print("Chức năng: Xóa nhân viên theo mã")

def cap_nhat_thong_tin():
    print("Chức năng: Cập nhật thông tin nhân viên")

def tim_theo_luong():
    print("Chức năng: Tìm nhân viên theo lương")

def sap_xep_theo_ten():
    print("Chức năng: Sắp xếp nhân viên theo họ tên")

def sap_xep_theo_thu_nhap():
    print("Chức năng: Sắp xếp nhân viên theo thu nhập")

def top5_thu_nhap():
    print("Chức năng: Xuất 5 nhân viên có thu nhập cao nhất")

def print_menu():
    print("\n=== QUẢN LÝ NHÂN SỰ TIỀN LƯƠNG ===")
    for key, describe in TASK.items():
        print(f"{key}. {describe}")
    print("0. Thoát")


while True:
    print_menu()
    choose = safe_input_int("Chọn chức năng: ")
    match choose:
        case 1: nhap_nhan_vien()
        case 2: xuat_danh_sach()
        case 3: tim_theo_ma()
        case 4: xoa_theo_ma()
        case 5: cap_nhat_thong_tin()
        case 6: tim_theo_luong()
        case 7: sap_xep_theo_ten()
        case 8: sap_xep_theo_thu_nhap()
        case 9: top5_thu_nhap()
        case 0:
            print("Thank you!")
            break
        case _: print("Chức năng không tồn tại, vui lòng nhập lại.")

