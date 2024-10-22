-- Tạo bảng Khách hàng
CREATE TABLE KhachHang (
    soThe VARCHAR(20) PRIMARY KEY,
    tenKH VARCHAR(50),
    maPIN VARCHAR(4)
);

-- Tạo bảng Tài khoản
CREATE TABLE TaiKhoan (
    soTK VARCHAR(20) PRIMARY KEY,
    loaiTK VARCHAR(20),
    soDu DECIMAL(15,2),
    soThe VARCHAR(20),
    FOREIGN KEY (soThe) REFERENCES KhachHang(soThe)
);

-- Tạo bảng GiaoDich
CREATE TABLE GiaoDich (
    giaoDichID VARCHAR(36) PRIMARY KEY,
    soTK VARCHAR(20) NOT NULL,
    loaiGD NVARCHAR(50) NOT NULL,
    soTien DECIMAL(18, 2) NOT NULL,
    soDuSauGD DECIMAL(18, 2) NOT NULL,
    thoiGian DATETIME NOT NULL,
    FOREIGN KEY (soTK) REFERENCES TaiKhoan(soTK)
);

-- Chèn dữ liệu mẫu cho bảng Khách hàng (10 records)
INSERT INTO KhachHang (soThe, tenKH, maPIN) VALUES
('1234567890', 'Nguyen Van A', '1234'),
('9876543210', 'Tran Thi B', '4321'),
('1122334455', 'Le Van C', '5544'),
('5566778899', 'Pham Thi D', '6677'),
('1011121314', 'Hoang Van E', '7788'),
('1516171819', 'Do Thi F', '8899'),
('2021222324', 'Vo Van G', '9900'),
('2526272829', 'Ngo Thi H', '0011'),
('3031323334', 'Ly Van I', '1122'),
('3536373839', 'Phan Thi J', '2233');

-- Chèn dữ liệu mẫu cho bảng Tài khoản (10 records)
INSERT INTO TaiKhoan (soTK, loaiTK, soDu, soThe) VALUES
('TK001', 'Tiet kiem', 1500000, '1234567890'),
('TK002', 'Thanh toan', 800000, '9876543210'),
('TK003', 'Tiet kiem', 2200000, '1122334455'),
('TK004', 'Thanh toan', 500000, '5566778899'),
('TK005', 'Tiet kiem', 1000000, '1011121314'),
('TK006', 'Thanh toan', 750000, '1516171819'),
('TK007', 'Tiet kiem', 3000000, '2021222324'),
('TK008', 'Thanh toan', 600000, '2526272829'),
('TK009', 'Tiet kiem', 1800000, '3031323334'),
('TK010', 'Thanh toan', 900000, '3536373839');


