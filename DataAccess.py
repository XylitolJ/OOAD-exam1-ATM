import pyodbc
from decimal import Decimal
import uuid
from datetime import date
from datetime import datetime

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
            str(giaoDich.soTien),  # Chuyển Decimal thành str
            str(giaoDich.soDu),    # Chuyển Decimal thành str
            giaoDich.thoiGianGiaoDich
        ))
        self.conn.commit()
