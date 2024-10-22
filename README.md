# Ví dụ ATM - Phân tích thiết kế hệ thống hướng đối tượng (OOAD)

# **Tài liệu chi tiết cho chương trình giả lập ATM**

# **Giới thiệu**

Chương trình giả lập ATM này được viết bằng ngôn ngữ Python, sử dụng thư viện PyQt5 để xây dựng giao diện đồ họa (GUI). Mục đích của chương trình là mô phỏng các chức năng cơ bản của một máy ATM thực tế, bao gồm khởi động máy, đăng nhập khách hàng, rút tiền, gửi tiền và truy vấn thông tin tài khoản.Chương trình được xây dựng theo kiến trúc 3 tầng:

- **Tầng Giao Diện (GUI Layer)**: Quản lý giao diện người dùng và các tương tác với người dùng.
- **Tầng Nghiệp Vụ (Business Layer)**: Xử lý logic nghiệp vụ và các quy tắc kinh doanh.
- **Tầng Truy Cập Dữ Liệu (Data Access Layer)**: Quản lý kết nối và tương tác với cơ sở dữ liệu.

# **Kiến trúc tổng quan**

## Sơ đồ lớp (Class Diagram)

![Sơ đồ lớp](https://i.imgur.com/nMu8Cil.png)

# Mô tả chi tiết các lớp


## **Tầng Giao Diện**

### **Lớp MayATM_GD**

- Chịu trách nhiệm quản lý toàn bộ giao diện của máy ATM.
- Quản lý các màn hình khác nhau như khởi động máy, đăng nhập khách hàng, giao dịch, tài khoản.
- Sử dụng QStackedWidget để chuyển đổi giữa các màn hình.

**Mã nguồn trích đoạn trong Start.py:**

```python
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
```

**Lớp MayATM_KhoiDongGD**

- Quản lý giao diện khởi động máy ATM.
- Cho phép nhân viên vận hành nhập số tiền khởi động ban đầu cho máy ATM.

**Mã nguồn trích đoạn trong Start.py:**

```python
class MayATM_KhoiDongGD(QWidget):
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.mayATM = mayATM_GD.mayATM
        self.setWindowTitle("Khởi động Máy ATM")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Địa chỉ máy ATM: {self.mayATM.diaChi}"))
        layout.addWidget(QLabel("Nhập số tiền khởi động máy:"))

        self.soTienKhoiDong_edit = QLineEdit()
        layout.addWidget(self.soTienKhoiDong_edit)

        # Thêm bàn phím số và nút khởi động...

        btn_khoi_dong = QPushButton("Khởi động")
        btn_khoi_dong.clicked.connect(self.khoiDongMay)
        layout.addWidget(btn_khoi_dong)
        self.setLayout(layout)
```

**Lớp KhachHangGD**

- Quản lý giao diện đăng nhập khách hàng.
- Cho phép khách hàng nhập số thẻ và mã PIN để truy cập tài khoản.

**Mã nguồn trích đoạn trong Start.py:**

```python
class KhachHangGD(QWidget):
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

        # Thêm bàn phím số và nút đăng nhập...

        btn_dang_nhap = QPushButton("Đăng nhập")
        btn_dang_nhap.clicked.connect(self.dangNhap)
        layout.addWidget(btn_dang_nhap)
        self.setLayout(layout)
```

**Lớp GiaoDichGD**

- Quản lý giao diện thực hiện các giao dịch.
- Cho phép khách hàng chọn rút tiền, gửi tiền hoặc xem số dư.

**Mã nguồn trích đoạn trong Start.py:**

```python
class GiaoDichGD(QWidget):
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
```

**Lớp TaiKhoanGD**

- Quản lý giao diện liên quan đến tài khoản.
- Hiển thị thông tin số dư, thực hiện rút và gửi tiền.

**Mã nguồn trích đoạn trong Start.py:**

```python
class TaiKhoanGD(QWidget):
    def __init__(self, mayATM_GD):
        super().__init__()
        self.mayATM_GD = mayATM_GD
        self.taiKhoan = None
        self.setWindowTitle("Tài khoản")

        self.layout = QVBoxLayout()
        self.label_thong_tin = QLabel()
        self.layout.addWidget(self.label_thong_tin)

        self.label_so_tien = QLabel("Nhập số tiền:")
        self.layout.addWidget(self.label_so_tien)
        self.soTien_edit = QLineEdit()
        self.layout.addWidget(self.soTien_edit)

        # Thêm bàn phím số và nút xác nhận...

        self.btn_xac_nhan = QPushButton("Xác nhận")
        self.btn_xac_nhan.clicked.connect(self.thucHienGiaoDich)
        self.layout.addWidget(self.btn_xac_nhan)

        self.btn_dong = QPushButton("Đóng")
        self.btn_dong.clicked.connect(self.dong)
        self.layout.addWidget(self.btn_dong)

        self.setLayout(self.layout)
```

## **Tầng Nghiệp Vụ**

### **Lớp MayATM**

- Quản lý trạng thái và thông tin của máy ATM.
- Có các phương thức để khởi động máy, cập nhật số tiền hiện tại của máy, đóng máy.

**Mã nguồn trích đoạn trong Business.py:**

```python
class MayATM:
    def __init__(self, diaChi):
        self.diaChi = diaChi
        self.trangThai = "Tắt"
        self.soTienHienTai = Decimal(0)
        self.nganHang = NganHang()

    def khoiDongMay(self, soTienKhoiTao):
        self.capNhatSoTien(soTienKhoiTao)
        self.nganHang.ketNoiDB()
        self.trangThai = "Hoạt động"
        print(f"Máy ATM đã khởi động với số tiền {soTienKhoiTao}.")

    def capNhatSoTien(self, soTien):
        self.soTienHienTai += Decimal(soTien)
```

**Lớp TaiKhoan**

- Quản lý thông tin tài khoản của khách hàng.
- Có các phương thức để gửi tiền, rút tiền, cập nhật tài khoản, tạo giao dịch.

**Mã nguồn trích đoạn trong Business.py:**

```python
class TaiKhoan:
    def __init__(self, soTaiKhoan, loaiTaiKhoan, soDu, khachHang=None):
        self.soTaiKhoan = soTaiKhoan
        self.loaiTaiKhoan = loaiTaiKhoan
        self.soDu = Decimal(soDu)
        self.giaoDich = None
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
```

**Lớp KhachHang**

- Quản lý thông tin khách hàng.
- Có các phương thức để kiểm tra mật khẩu, lấy thông tin khách hàng và tài khoản.

**Mã nguồn trích đoạn trong Business.py:**

```python
class KhachHang:
    def __init__(self):
        self.tenKhachHang = ""
        self.maPIN = ""
        self.soThe = ""
        self.taiKhoan = None
        self.nganHangDB = NganHangDB()
        self.nganHangDB.ketNoi()

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
```

**Lớp GiaoDich**

- Quản lý thông tin giao dịch.
- Có các phương thức để tạo mới và gán thông tin giao dịch.

**Mã nguồn trích đoạn trong Business.py:**

```python
class GiaoDich:
    def __init__(self):
        self.giaoDichID = None
        self.thoiGianGiaoDich = None
        self.loaiGiaoDich = None
        self.soTien = None
        self.soDu = None
        self.soTaiKhoan = None

    def taoMoi(self):
        self.giaoDichID = str(uuid.uuid4())
        self.thoiGianGiaoDich = datetime.now()

    def ganThongTin(self, loaiGD, soTien, soDu, soTK):
        self.loaiGiaoDich = loaiGD
        self.soTien = Decimal(soTien)
        self.soDu = Decimal(soDu)
        self.soTaiKhoan = soTK
```

**Lớp NganHang**

- Quản lý kết nối đến cơ sở dữ liệu thông qua NganHangDB.

**Mã nguồn trích đoạn trong Business.py:**

```python
class NganHang:
     def __init__(self):
        self.nganHangDB = NganHangDB()

     def ketNoiDB(self):
        self.nganHangDB.ketNoi()

     def dongKetNoiDB(self):
        self.nganHangDB.dongKetNoi()
```

## **Tầng Truy Cập Dữ Liệu**

### **Lớp NganHangDB**

- Quản lý kết nối và tương tác với cơ sở dữ liệu.
- Có các phương thức để đọc thông tin khách hàng, tài khoản, cập nhật tài khoản, ghi nhận giao dịch.

**Mã nguồn trích đoạn trong DataAccess.py:**

```python
class NganHangDB:
    def __init__(self):
        self.conn = None

    def ketNoi(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=Z790\\SQLEXPRESS;'
                'DATABASE=ATM_DB;'
                'Trusted_Connection=yes;'
            )
        except Exception as e:
            print("Kết nối thất bại:", e)

    def dongKetNoi(self):
        if self.conn:
            self.conn.close()

    def docKhachHang(self, soThe, maPIN):
        cursor = self.conn.cursor()
        query = "SELECT * FROM KhachHang WHERE soThe = ? AND maPIN = ?"
        cursor.execute(query, (soThe, maPIN))
        result = cursor.fetchone()
        return result

    def docTaiKhoan(self, soThe):
        cursor = self.conn.cursor()
        query = "SELECT * FROM TaiKhoan WHERE soThe = ?"
        cursor.execute(query, (soThe,))
        result = cursor.fetchone()
        if result:
            result.soDu = Decimal(result.soDu)
        return result

    def capNhatTaiKhoan(self, soTK, soDu):
        cursor = self.conn.cursor()
        query = "UPDATE TaiKhoan SET soDu = ? WHERE soTK = ?"
        cursor.execute(query, (str(soDu), soTK))
        self.conn.commit()

    def capNhatGiaoDich(self, giaoDich):
        cursor = self.conn.cursor()
        query = """
        INSERT INTO GiaoDich (giaoDichID, soTK, loaiGD, soTien, soDuSauGD, thoiGian)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            giaoDich.giaoDichID,
            giaoDich.soTaiKhoan,
            giaoDich.loaiGiaoDich,
            str(giaoDich.soTien),
            str(giaoDich.soDu),
            giaoDich.thoiGianGiaoDich
        ))
        self.conn.commit()
```

# **Mô tả chi tiết các Use Case**

## **Use Case 1: Khởi động máy ATM**

### **Mô tả**

Nhân viên vận hành khởi động máy ATM bằng cách nhập số tiền khởi động ban đầu. Máy ATM sẽ cập nhật số tiền hiện tại, kết nối với cơ sở dữ liệu và chuyển trạng thái sang "Hoạt động".

### **Luồng sự kiện**

- Nhân viên vận hành mở ứng dụng và màn hình khởi động được hiển thị.
- Nhân viên nhập số tiền khởi động ban đầu vào máy.
- Hệ thống cập nhật số tiền hiện tại của máy ATM.
- Máy ATM kết nối với cơ sở dữ liệu ngân hàng.
- Máy ATM chuyển trạng thái sang "Hoạt động".

### **Mã nguồn minh họa**

**Phương thức khoiDongMay trong lớp MayATM_KhoiDongGD (Start.py):**

```python
def khoiDongMay(self):
    try:
        soTien = Decimal(self.soTienKhoiDong_edit.text())
        self.mayATM.khoiDongMay(soTien)
        self.mayATM_GD.hienThiKhachHang()
    except Exception as e:
        print(f"Lỗi: {e}")
        QMessageBox.warning(self, "Lỗi", "Số tiền không hợp lệ!")
```

**Phương thức khoiDongMay trong lớp MayATM (Business.py):**

```python
def khoiDongMay(self, soTienKhoiTao):
    self.capNhatSoTien(soTienKhoiTao)
    self.nganHang.ketNoiDB()
    self.trangThai = "Hoạt động"
    print(f"Máy ATM đã khởi động với số tiền {soTienKhoiTao}.")
```

## **Use Case 2: Đăng nhập khách hàng**

### **Mô tả**

Khách hàng sử dụng máy ATM và nhập số thẻ cùng mã PIN để truy cập tài khoản của mình. Hệ thống kiểm tra thông tin đăng nhập và nếu hợp lệ, khách hàng sẽ được chuyển đến màn hình giao dịch.

### **Luồng sự kiện**

- Khách hàng nhập số thẻ và mã PIN trên màn hình.
- Hệ thống kiểm tra thông tin đăng nhập với cơ sở dữ liệu.
- Nếu thông tin hợp lệ, hệ thống tải thông tin khách hàng và tài khoản.
- Chuyển đến màn hình giao dịch.

### **Mã nguồn minh họa**

**Phương thức dangNhap trong lớp KhachHangGD (Start.py):**

```python
def dangNhap(self):
    soThe = self.soThe_edit.text()
    maPIN = self.maPIN_edit.text()
    khachHang = KhachHang()
    if khachHang.layKhachHang(soThe, maPIN):
        self.mayATM_GD.khachHang = khachHang
        self.mayATM_GD.taiKhoan = khachHang.layTaiKhoan(soThe)
        self.mayATM_GD.giaoDichGD.hienThi()
        self.mayATM_GD.stacked_widget.setCurrentWidget(self.mayATM_GD.giaoDichGD)
    else:
        QMessageBox.warning(self, "Lỗi", "Số thẻ hoặc mã PIN không đúng.")
```

**Phương thức layKhachHang trong lớp KhachHang (Business.py):**

```python
def layKhachHang(self, soThe, maPIN):
    khachHangData = self.nganHangDB.docKhachHang(soThe, maPIN)
    if khachHangData:
        self.soThe = khachHangData.soThe
        self.tenKhachHang = khachHangData.tenKH
        self.maPIN = khachHangData.maPIN
        return self
    return None
```

## **Use Case 3: Rút tiền**

### **Mô tả**

Khách hàng thực hiện giao dịch rút tiền từ tài khoản của mình. Hệ thống kiểm tra số dư và số tiền trong máy ATM để đảm bảo khả năng thực hiện giao dịch.

### **Luồng sự kiện**

- Khách hàng chọn chức năng "Rút tiền".
- Khách hàng nhập số tiền muốn rút.
- Hệ thống kiểm tra số dư tài khoản và số tiền hiện có trong máy ATM.
- Nếu đủ điều kiện, hệ thống thực hiện giao dịch, cập nhật số dư tài khoản và số tiền trong máy ATM.
- Ghi nhận giao dịch vào cơ sở dữ liệu.
- Hiển thị thông tin giao dịch cho khách hàng.

### **Mã nguồn minh họa**

**Phương thức thucHienGiaoDich trong lớp TaiKhoanGD (Start.py):**

```python
def thucHienGiaoDich(self):
    try:
        soTien = Decimal(self.soTien_edit.text())
        if self.loai_giao_dich == 'rut':
            ket_qua = self.taiKhoan.rutTien(soTien)
            if ket_qua == "Rút tiền thành công.":
                QMessageBox.information(self, "Thông báo", ket_qua)
                self.hienThiThongTin()
            else:
                QMessageBox.warning(self, "Thông báo", ket_qua)
    except Exception as e:
        print(f"Lỗi: {e}")
        QMessageBox.warning(self, "Lỗi", f"Số tiền không hợp lệ: {str(e)}")
```

**Phương thức rutTien trong lớp TaiKhoan (Business.py):**

```python
def rutTien(self, soTien):
    soTien = Decimal(soTien)
    if self.soDu >= soTien:
        self.soDu -= soTien
        self.capNhatTaiKhoan(self.soTaiKhoan, self.soDu)
        self.taoGiaoDich("Rút tiền", soTien, self.soDu)
        return "Rút tiền thành công."
    else:
        return "Số dư không đủ."
```

## **Use Case 4: Gửi tiền**

### **Mô tả**

Khách hàng thực hiện giao dịch gửi tiền vào tài khoản của mình. Hệ thống cập nhật số dư tài khoản và số tiền trong máy ATM.

### **Luồng sự kiện**

- Khách hàng chọn chức năng "Gửi tiền".
- Khách hàng nhập số tiền muốn gửi.
- Hệ thống cập nhật số dư tài khoản và số tiền trong máy ATM.
- Ghi nhận giao dịch vào cơ sở dữ liệu.
- Hiển thị thông tin giao dịch cho khách hàng.

### **Mã nguồn minh họa**

**Phương thức thucHienGiaoDich trong lớp TaiKhoanGD (Start.py):**

```python
def thucHienGiaoDich(self):
    try:
        soTien = Decimal(self.soTien_edit.text())
        if self.loai_giao_dich == 'gui':
            ket_qua = self.taiKhoan.guiTien(soTien)
            if ket_qua == "Gửi tiền thành công.":
                QMessageBox.information(self, "Thông báo", ket_qua)
                self.hienThiThongTin()
            else:
                QMessageBox.warning(self, "Thông báo", ket_qua)
    except Exception as e:
        print(f"Lỗi: {e}")
        QMessageBox.warning(self, "Lỗi", f"Số tiền không hợp lệ: {str(e)}")
```

**Phương thức guiTien trong lớp TaiKhoan (Business.py):**

```python
def guiTien(self, soTien):
    soTien = Decimal(soTien)
    self.soDu += soTien
    self.capNhatTaiKhoan(self.soTaiKhoan, self.soDu)
    self.taoGiaoDich("Gửi tiền", soTien, self.soDu)
    return "Gửi tiền thành công."
```

## **Use Case 5: Truy vấn thông tin tài khoản**

### **Mô tả**

Khách hàng muốn xem số dư hiện tại của tài khoản.

### **Luồng sự kiện**

- Khách hàng chọn chức năng "Xem số dư".
- Hệ thống lấy thông tin số dư của tài khoản từ cơ sở dữ liệu.
- Hiển thị số dư cho khách hàng.

### **Mã nguồn minh họa**

**Phương thức hienThiThongTin trong lớp TaiKhoanGD (Start.py):**

```python
def hienThiThongTin(self):
    self.taiKhoan = self.mayATM_GD.taiKhoan
    if self.taiKhoan:
        soDu_formatted = "{:,.2f}".format(self.taiKhoan.soDu)
        self.label_thong_tin.setText(f"Số dư hiện tại: {soDu_formatted} VND")
    else:
        self.label_thong_tin.setText("Không có thông tin tài khoản")

    self.label_so_tien.hide()
    self.soTien_edit.hide()
    self.btn_xac_nhan.hide()
    self.mayATM_GD.stacked_widget.setCurrentWidget(self)
```

Chương trình giả lập ATM này cung cấp một mô hình cơ bản về cách thức hoạt động của một máy ATM thực tế, từ khởi động máy, đăng nhập khách hàng đến thực hiện các giao dịch cơ bản. Việc phân chia rõ ràng giữa các tầng giao diện, nghiệp vụ và truy cập dữ liệu giúp cho code được tổ chức tốt, dễ dàng bảo trì và mở rộng trong tương lai.
