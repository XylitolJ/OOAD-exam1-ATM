from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from decimal import Decimal
from Business import MayATM, KhachHang, TaiKhoan, GiaoDich
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QStackedWidget, QGridLayout)
from datetime import date, datetime

# Tạo lớp FocusedLineEdit kế thừa từ QLineEdit
class FocusedLineEdit(QLineEdit):
    focus_in = pyqtSignal()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focus_in.emit()

class MayATM_GD(QWidget):
    def __init__(self, mayATM):
        super().__init__()
        self.mayATM = mayATM
        self.khachHang = None
        self.taiKhoan = None

        self.stacked_widget = QStackedWidget()

        self.mayATM_KhoiDongGD = MayATM_KhoiDongGD(self)
        self.khachHangGD = KhachHangGD(self)
        self.giaoDichGD = GiaoDichGD(self)
        self.taiKhoanGD = TaiKhoanGD(self)

        self.stacked_widget.addWidget(self.mayATM_KhoiDongGD)
        self.stacked_widget.addWidget(self.khachHangGD)
        self.stacked_widget.addWidget(self.giaoDichGD)
        self.stacked_widget.addWidget(self.taiKhoanGD)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.setWindowTitle("Máy ATM")
        self.hienThiKhoiDong()

    def hienThi(self):
        self.show()

    def hienThiKhoiDong(self):
        self.stacked_widget.setCurrentWidget(self.mayATM_KhoiDongGD)

    def hienThiKhachHang(self):
        self.stacked_widget.setCurrentWidget(self.khachHangGD)

    def hienThiGiaoDich(self):
        self.giaoDichGD.hienThi()
        self.stacked_widget.setCurrentWidget(self.giaoDichGD)

    def hienThiTaiKhoan(self):
        self.stacked_widget.setCurrentWidget(self.taiKhoanGD)

    def dong(self):
        self.close()

class MayATM_KhoiDongGD(QWidget): # biểu diễn tương tác giữa nhân viên vận hành và use case Khởi động hệ thống
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.mayATM = mayATM_GD.mayATM
        self.setWindowTitle("Khởi động Máy ATM")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Địa chỉ máy ATM: {self.mayATM.diaChi}"))  # Thêm dòng hiển thị địa chỉ máy

        layout.addWidget(QLabel("Nhập số tiền khởi động máy:"))

        self.soTienKhoiDong_edit = QLineEdit()
        # self.soTienKhoiDong_edit.setFont(QFont("Arial", 16))
        layout.addWidget(self.soTienKhoiDong_edit)

        # Bàn phím số
        grid_layout = QGridLayout()
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '<-',
        ]
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, button in zip(positions, buttons):
            button_widget = QPushButton(button)
            # button_widget.setFont(QFont("Arial", 16))
            button_widget.clicked.connect(lambda _, b=button: self.button_clicked(b))
            grid_layout.addWidget(button_widget, *position)

        layout.addLayout(grid_layout)

        btn_khoi_dong = QPushButton("Khởi động")
        # btn_khoi_dong.setFont(QFont("Arial", 16))
        btn_khoi_dong.clicked.connect(self.khoiDongMay)
        layout.addWidget(btn_khoi_dong)
        self.setLayout(layout)

    def button_clicked(self, text):
        if text == '<-':
            self.soTienKhoiDong_edit.backspace()
        else:
            self.soTienKhoiDong_edit.insert(text)

    def khoiDongMay(self): #chính là hàm hiểnthi() trong lớp MayATM_GD
        try:
            soTien = Decimal(self.soTienKhoiDong_edit.text())
            # self.mayATM.capNhatSoTien(soTien)
            self.mayATM.khoiDongMay(soTien)
            self.mayATM_GD.hienThiKhachHang()
        except Exception as e:
            print(f"Lỗi: {e}")
            QMessageBox.warning(self, "Lỗi", "Số tiền không hợp lệ!")

    def dong(self): #TODO gọi hàm dongMay() trong lớp MayATM
        self.mayATM_GD.dong()

class KhachHangGD(QWidget): #biểu diễn giao diện tương tác giữa khách hàng và use case Đăng nhập, Đăngnhập không hợp lệ
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.setWindowTitle("Đăng nhập")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Số thẻ:"))
        self.soThe_edit = FocusedLineEdit()
        layout.addWidget(self.soThe_edit)

        layout.addWidget(QLabel("Mã PIN:"))
        self.maPIN_edit = FocusedLineEdit()
        self.maPIN_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.maPIN_edit)

        # Biến lưu trữ ô nhập liệu hiện tại
        self.current_edit = self.soThe_edit

        # Kết nối sự kiện focus vào phương thức cập nhật current_edit
        self.soThe_edit.focus_in.connect(lambda: self.set_current_edit(self.soThe_edit))
        self.maPIN_edit.focus_in.connect(lambda: self.set_current_edit(self.maPIN_edit))

        # Bàn phím số
        grid_layout = QGridLayout()
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '<-',
        ]
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, button in zip(positions, buttons):
            button_widget = QPushButton(button)
            button_widget.setFont(QFont("Arial", 16))
            button_widget.clicked.connect(lambda _, b=button: self.button_clicked(b))
            grid_layout.addWidget(button_widget, *position)

        layout.addLayout(grid_layout)

        btn_dang_nhap = QPushButton("Đăng nhập")
        btn_dang_nhap.clicked.connect(self.dangNhap)
        layout.addWidget(btn_dang_nhap)
        self.setLayout(layout)

    def set_current_edit(self, edit):
        self.current_edit = edit

    def button_clicked(self, text):
        if text == '<-':
            # Xóa ký tự cuối
            current_text = self.current_edit.text()
            self.current_edit.setText(current_text[:-1])
        else:
            # Thêm ký tự vào cuối
            self.current_edit.setText(self.current_edit.text() + text)

    def dangNhap(self):
        soThe = self.soThe_edit.text()
        maPIN = self.maPIN_edit.text()
        khachHang = KhachHang()
        if khachHang.layKhachHang(soThe, maPIN):
            self.mayATM_GD.khachHang = khachHang
            self.mayATM_GD.taiKhoan = khachHang.layTaiKhoan(soThe)
            # Hiển thị lời chào
            self.mayATM_GD.giaoDichGD.hienThi()
            self.mayATM_GD.stacked_widget.setCurrentWidget(self.mayATM_GD.giaoDichGD)
        else:
            QMessageBox.warning(self, "Lỗi", "Số thẻ hoặc mã PIN không đúng.")

    def dong(self):
        self.mayATM_GD.dong()

class GiaoDichGD(QWidget): # biểu diễn tương tác giữa khách hàng và use case Rút tiền, Gửi tiền
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.setWindowTitle("Giao dịch")

        self.layout = QVBoxLayout()
        self.label_chao = QLabel("")
        self.layout.addWidget(self.label_chao)
        self.layout.addWidget(QLabel("Vui lòng chọn giao dịch:"))

        btn_rut_tien = QPushButton("Rút tiền")
        btn_rut_tien.clicked.connect(self.rutTien)
        self.layout.addWidget(btn_rut_tien)

        btn_gui_tien = QPushButton("Gửi tiền")
        btn_gui_tien.clicked.connect(self.guiTien)
        self.layout.addWidget(btn_gui_tien)

        btn_xem_so_du = QPushButton("Xem số dư")
        btn_xem_so_du.clicked.connect(self.xemSoDu)
        self.layout.addWidget(btn_xem_so_du)

        btn_thoat = QPushButton("Thoát")
        btn_thoat.clicked.connect(self.dong)
        self.layout.addWidget(btn_thoat)

        self.setLayout(self.layout)

    def hienThi(self):
        ten_khach_hang = self.mayATM_GD.khachHang.tenKhachHang if self.mayATM_GD.khachHang else ""
        self.label_chao.setText(f"Xin chào, {ten_khach_hang}!")
        self.mayATM_GD.stacked_widget.setCurrentWidget(self)

    def rutTien(self):
        self.mayATM_GD.taiKhoanGD.hienThiRutTien()

    def guiTien(self):
        self.mayATM_GD.taiKhoanGD.hienThiGuiTien()

    def xemSoDu(self):
        self.mayATM_GD.taiKhoanGD.hienThiThongTin()

    def dong(self):
        self.mayATM_GD.hienThiKhachHang()

class TaiKhoanGD(QWidget): # biểu diễn tương tác giữa khách hàng và use case Truy vấn thông tin tài khoản
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.taiKhoan = None
        self.setWindowTitle("Tài khoản")

        self.layout = QVBoxLayout()
        self.label_thong_tin = QLabel()
        self.layout.addWidget(self.label_thong_tin)

        # Thêm phn nhập số tiền và bàn phím số
        self.label_so_tien = QLabel("Nhập số tiền:")
        self.layout.addWidget(self.label_so_tien)
        self.soTien_edit = QLineEdit()
        self.layout.addWidget(self.soTien_edit)

        grid_layout = QGridLayout()
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '<-',
        ]
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, button in zip(positions, buttons):
            button_widget = QPushButton(button)
            button_widget.setFont(QFont("Arial", 16))
            button_widget.clicked.connect(lambda _, b=button: self.button_clicked(b))
            grid_layout.addWidget(button_widget, *position)

        self.layout.addLayout(grid_layout)

        # Nút xác nhận
        self.btn_xac_nhan = QPushButton("Xác nhận")
        self.btn_xac_nhan.clicked.connect(self.thucHienGiaoDich)
        self.layout.addWidget(self.btn_xac_nhan)

        # Nút đóng
        self.btn_dong = QPushButton("Đóng")
        self.btn_dong.clicked.connect(self.dong)
        self.layout.addWidget(self.btn_dong)

        self.setLayout(self.layout)

        self.loai_giao_dich = None  # 'rut' hoặc 'gui'

    def button_clicked(self, text):
        if text == '<-':
            self.soTien_edit.backspace()
        else:
            self.soTien_edit.insert(text)

    def hienThiThongTin(self):
        self.taiKhoan = self.mayATM_GD.taiKhoan
        if self.taiKhoan:
            soDu_formatted = "{:,.2f}".format(self.taiKhoan.soDu)
            self.label_thong_tin.setText(f"Số dư hiện tại: {soDu_formatted} VND")
        else:
            self.label_thong_tin.setText("Không có thông tin tài khoản")

        # Ẩn các widget liên quan đến giao dịch
        self.label_so_tien.hide()
        self.soTien_edit.hide()
        self.btn_xac_nhan.hide()
        self.mayATM_GD.stacked_widget.setCurrentWidget(self)

    def hienThiRutTien(self):
        self.taiKhoan = self.mayATM_GD.taiKhoan
        self.loai_giao_dich = 'rut'
        self.label_thong_tin.setText("Nhập số tiền cần rút:")
        self.label_so_tien.show()
        self.soTien_edit.show()
        self.btn_xac_nhan.show()
        self.soTien_edit.clear()
        self.mayATM_GD.stacked_widget.setCurrentWidget(self)

    def hienThiGuiTien(self):
        self.taiKhoan = self.mayATM_GD.taiKhoan
        self.loai_giao_dich = 'gui'
        self.label_thong_tin.setText("Nhập số tiền cần gửi:")
        self.label_so_tien.show()
        self.soTien_edit.show()
        self.btn_xac_nhan.show()
        self.soTien_edit.clear()
        self.mayATM_GD.stacked_widget.setCurrentWidget(self)

    def thucHienGiaoDich(self):
        try:
            soTien = Decimal(self.soTien_edit.text())
            if self.loai_giao_dich == 'rut':
                giaoDich = GiaoDich()
                giaoDich.taoMoi()
                giaoDich.ganThongTin(
                    "Rút tiền",
                    soTien,
                    self.taiKhoan.soDu - soTien,
                    self.taiKhoan.soTaiKhoan
                )
                ket_qua = self.taiKhoan.rutTien(soTien)
                if ket_qua == "Rút tiền thành công.":
                    QMessageBox.information(self, "Thông báo", ket_qua)
                    self.hienThiThongTinGiaoDich(giaoDich)
                    self.hienThiThongTin()
                else:
                    QMessageBox.warning(self, "Thông báo", ket_qua)
            elif self.loai_giao_dich == 'gui':
                giaoDich = GiaoDich()
                giaoDich.taoMoi()
                giaoDich.ganThongTin(
                    "Gửi tiền",
                    soTien,
                    self.taiKhoan.soDu + soTien,
                    self.taiKhoan.soTaiKhoan
                )
                ket_qua = self.taiKhoan.guiTien(soTien)
                if ket_qua == "Gửi tiền thành công.":
                    QMessageBox.information(self, "Thông báo", ket_qua)
                    self.hienThiThongTinGiaoDich(giaoDich)
                    self.hienThiThongTin()
                else:
                    QMessageBox.warning(self, "Thông báo", ket_qua)
        except Exception as e:
            print(f"Lỗi: {e}")
            QMessageBox.warning(self, "Lỗi", f"Số tiền không hợp lệ: {str(e)}")

    def dong(self):
        self.mayATM_GD.hienThiGiaoDich()

    def hienThiThongTinGiaoDich(self, giaoDich):
        if giaoDich:
            thongTin = f"Số tài khoản: {giaoDich.soTaiKhoan}\n"
            thongTin += f"ID giao dịch: {giaoDich.giaoDichID[:8]}\n"
            thongTin += f"Loại giao dịch: {giaoDich.loaiGiaoDich}\n"
            thongTin += f"Số tiền: {giaoDich.soTien:,.2f} VND\n"
            thongTin += f"Số dư sau giao dịch: {giaoDich.soDu:,.2f} VND\n"
            thongTin += f"Thời gian giao dịch: {giaoDich.thoiGianGiaoDich}"
            QMessageBox.information(self, "Thông tin giao dịch", thongTin)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mayATM = MayATM("123 Đường ABC")  # Địa chỉ máy ATM
    app.setFont(QFont("Arial", 14))  # Áp dụng font cho toàn bộ ứng dụng
    mayATM_GD = MayATM_GD(mayATM)
    mayATM_GD.hienThi()
    sys.exit(app.exec_())
