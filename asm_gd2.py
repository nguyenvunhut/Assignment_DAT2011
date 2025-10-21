from quanly import QuanLyNhanSu

def hien_thi_menu():
    """Hiển thị menu chức năng cho người dùng từ dictionary."""
    menu_options = {
        1: "Thêm nhân viên mới",
        2: "Hiển thị danh sách nhân viên",
        3: "Tìm nhân viên theo mã",
        4: "Xóa nhân viên",
        5: "Cập nhật thông tin nhân viên",
        6: "Tìm nhân viên theo khoảng lương",
        7: "Sắp xếp nhân viên theo họ tên",
        8: "Sắp xếp nhân viên theo thu nhập",
        9: "Hiển thị top 5 nhân viên thu nhập cao nhất",
        0: "Thoát chương trình"
    }
    
    print("\n--- CHƯƠNG TRÌNH QUẢN LÝ NHÂN SỰ ---")
    for key, value in menu_options.items():
        print(f"{key}. {value}")
    print("------------------------------------")
    return menu_options

if __name__ == "__main__":
    ql_nhansu = QuanLyNhanSu()
    ql_nhansu.set_file_type()
    while True:
        menu_options = hien_thi_menu()
        try:
            lua_chon = int(input("Vui lòng chọn một chức năng: "))
            
            match lua_chon:
                case 1:
                    ql_nhansu.them_nhan_vien()
                case 2:
                    ql_nhansu.xuat_danh_sach_all()
                case 3:
                    ma_nv = input("Nhập mã nhân viên cần tìm: ").strip()
                    nv = ql_nhansu.tim_nhan_vien_theo_ma(ma_nv)
                    if nv:
                        nv.xuat_thong_tin()
                    else:
                        print(f"Không tìm thấy nhân viên có mã {ma_nv}")
                case 4:
                    ma_nv = input("Nhập mã nhân viên cần xóa: ").strip().upper()
                    ql_nhansu.xoa_nhan_vien_theo_ma(ma_nv)
                case 5:
                    ql_nhansu.cap_nhat_thong_tin()
                case 6:
                    ql_nhansu.tim_theo_khoang_luong()
                case 7:
                    ql_nhansu.sap_xep_theo_ten()
                case 8:
                    ql_nhansu.sap_xep_theo_thu_nhap()
                case 9:
                    ql_nhansu.top_5_thu_nhap_cao()
                case 0:
                    print("Cảm ơn đã sử dụng chương trình. Tạm biệt!")
                    break
                case _:
                    print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")