from DataAccess import NganHangDB
from decimal import Decimal
from datetime import datetime
import uuid

class MayATM:
    def __init__(self, diaChi):
        self.diaChi = diaChi
        self.trangThai = "Tắt"  # Khởi tạo trạng thái là "Tắt"
        self.soTienHienTai = Decimal(0)  # Khởi tạo số tiền là 0
        self.nganHang = NganHang()


    def khoiDongMay(self, soTienKhoiTao):
        self.capNhatSoTien(soTienKhoiTao)
        self.nganHang.ketNoiDB()
        self.trangThai = "Hoạt động"
        print(f"Máy ATM đã khởi động với số tiền {soTienKhoiTao}.")

    def dongMay(self):
        self.nganHang.dongKetNoiDB()
        self.trangThai = "Đang bảo trì"  # Có thể đặt trạng thái là "Đang bảo trì" trước khi tắt hoàn toàn
        self.tatMay() # gọi phương thức tatMay()
        print(f"Máy ATM đã được tắt, ")

    def capNhatSoTien(self, soTien):
        self.soTienHienTai += Decimal(soTien)

    def tatMay(self):
        self.trangThai = "Tắt"
        self.soTienHienTai = Decimal(0) # reset số tiền về 0
        # Thêm các xử lý cần thiết để tắt hoàn toàn máy ATM (ví dụ: tắt nguồn, ...)

class TaiKhoan:
    def __init__(self, soTaiKhoan, loaiTaiKhoan, soDu, khachHang=None):
        self.soTaiKhoan = soTaiKhoan
        self.loaiTaiKhoan = loaiTaiKhoan
        self.soDu = Decimal(soDu)
        self.giaoDich = None # None thay vì GiaoDich() -> vì nguyên tắc thiết kế "lazy initialization" (khởi tạo trễ).
        self.khachHang = khachHang
        self.nganHangDB = NganHangDB()
        self.nganHangDB.ketNoi()

    def guiTien(self, soTien):
        soTien = Decimal(soTien)
        self.soDu += soTien
        self.capNhatTaiKhoan(self.soTaiKhoan, self.soDu)
        self.taoGiaoDich("Gửi tiền", soTien, self.soDu)
        return "Gửi tiền thành công."

    def rutTien(self, soTien):
        soTien = Decimal(soTien)
        if self.soDu >= soTien:
            self.soDu -= soTien
            self.capNhatTaiKhoan(self.soTaiKhoan, self.soDu)
            self.taoGiaoDich("Rút tiền", soTien, self.soDu)
            return "Rút tiền thành công."
        else:
            return "Số dư không đủ."

    def capNhatTaiKhoan(self, soTaiKhoan, soDu):
        self.nganHangDB.capNhatTaiKhoan(soTaiKhoan, soDu)

    def taoGiaoDich(self, loaiGD, soTien, soDu):
        giaoDich = GiaoDich()
        giaoDich.taoMoi()
        giaoDich.ganThongTin(loaiGD, soTien, soDu, self.soTaiKhoan)
        self.nganHangDB.capNhatGiaoDich(giaoDich)


class KhachHang:
    def __init__(self):
        self.tenKhachHang = ""
        self.maPIN = ""
        self.soThe = ""
        self.taiKhoan = None
        self.nganHangDB = NganHangDB()
        self.nganHangDB.ketNoi()

    def kiemTraMatKhau(self, maPIN):
        return self.layKhachHang(self.soThe, maPIN)

    def layKhachHang(self, soThe, maPIN):
        khachHangData = self.nganHangDB.docKhachHang(soThe, maPIN)
        if khachHangData:
            self.soThe = khachHangData.soThe
            self.tenKhachHang = khachHangData.tenKH
            self.maPIN = khachHangData.maPIN
            return self
        return None

    def layTaiKhoan(self, soThe):
        taiKhoanData = self.nganHangDB.docTaiKhoan(soThe)
        if taiKhoanData:
            self.taiKhoan = TaiKhoan(
                soTaiKhoan=taiKhoanData.soTK,
                loaiTaiKhoan=taiKhoanData.loaiTK,
                soDu=taiKhoanData.soDu,
                khachHang=self
            )
            return self.taiKhoan
        return None

class GiaoDich:
    def __init__(self):
        self.giaoDichID = None
        self.thoiGianGiaoDich = None  # Sử dụng datetime
        self.loaiGiaoDich = None
        self.soTien = None
        self.soDu = None
        self.soTaiKhoan = None

    def taoMoi(self):
        self.giaoDichID = str(uuid.uuid4())
        self.thoiGianGiaoDich = datetime.now()  # Lưu datetime hiện tại

    def ganThongTin(self, loaiGD, soTien, soDu, soTK):
        self.loaiGiaoDich = loaiGD
        self.soTien = Decimal(soTien)
        self.soDu = Decimal(soDu)
        self.soTaiKhoan = soTK

class NganHang:
     def __init__(self):
        self.nganHangDB = NganHangDB()

     def ketNoiDB(self):
        self.nganHangDB.ketNoi()

     def dongKetNoiDB(self):
        self.nganHangDB.dongKetNoi()





