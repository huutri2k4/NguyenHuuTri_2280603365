import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đảm bảo rằng 'ui.rsa' có thể được import.
# Nếu 'ui' là một thư mục và 'rsa.py' nằm trong đó, cấu trúc này là đúng.
# Nếu 'rsa.py' nằm trực tiếp trong cùng thư mục với script này, bạn có thể cần thay đổi thành 'from rsa import Ui_MainWindow'
from ui.ecc import Ui_MainWindow 
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối các nút với các hàm xử lý API
        self.ui.btngenkey.clicked.connect(self.call_api_gen_keys)
        self.ui.btnsign.clicked.connect(self.call_api_sign)
        self.ui.btnverify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        """
        Gọi API để tạo cặp khóa RSA mới.
        Hiển thị thông báo thành công hoặc lỗi.
        """
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data.get("message", "Keys generated successfully!")) # Sử dụng .get() để an toàn hơn
                msg.exec_()
            else:
                # Xử lý lỗi từ phản hồi API
                error_message = response.json().get("error", "Unknown error generating keys.")
                print(f"Error while calling API (status {response.status_code}): {error_message}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Failed to generate keys: {error_message}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi kết nối hoặc HTTP
            print(f"Connection Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Network error: Could not connect to API. Is the server running? ({e})")
            msg.exec_()

    
    def call_api_sign(self):
        """
        Gọi API để ký một thông điệp.
        Hiển thị chữ ký và thông báo.
        """
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {
            "message": self.ui.txtinfo.toPlainText() # Giả định txt_info là trường nhập liệu cho thông điệp
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtsignature.setText(data.get("signature", ""))

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                # Xử lý lỗi nếu API trả về trạng thái không phải 200
                error_message = response.json().get("error", "Unknown error signing.")
                print(f"Error while calling API (status {response.status_code}): {error_message}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Failed to sign: {error_message}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi kết nối
            print(f"Connection Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Network error: Could not connect to API. Is the server running? ({e})")
            msg.exec_()

    def call_api_verify(self):
        """
        Gọi API để xác minh chữ ký của một thông điệp.
        Hiển thị kết quả xác minh (thành công/thất bại) và thông báo.
        """
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txtinfo.toPlainText(),
            "signature": self.ui.txtsignature.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_verified", False): # Sử dụng .get() và mặc định False
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning) # Thay đổi icon để thể hiện thất bại
                    msg.setText("Verified Fail")
                    msg.exec_()
            else: 
                # Xử lý lỗi nếu API trả về trạng thái không phải 200
                error_message = response.json().get("error", "Unknown error verifying.")
                print(f"Error while calling API (status {response.status_code}): {error_message}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Failed to verify: {error_message}")
                msg.exec_()

        except requests.exceptions.RequestException as e:
            # Xử lý lỗi kết nối
            print(f"Connection Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Network error: Could not connect to API. Is the server running? ({e})")
            msg.exec_()

# Khối chính để chạy ứng dụng PyQt5
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())