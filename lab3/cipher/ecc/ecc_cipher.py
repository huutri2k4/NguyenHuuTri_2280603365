import ecdsa, os

# Kiểm tra và tạo thư mục lưu trữ khóa nếu chưa tồn tại
if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        """
        Tạo cặp khóa riêng tư và khóa công khai ECC,
        sau đó lưu chúng vào các tệp .pem.
        """
        # Tạo khóa riêng tư (SigningKey)
        sk = ecdsa.SigningKey.generate()
        # Lấy khóa công khai (VerifyingKey) từ khóa riêng tư
        vk = sk.get_verifying_key()

        # Lưu khóa riêng tư vào file privateKey.pem
        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())

        # Lưu khóa công khai vào file publicKey.pem
        with open('cipher/ecc/keys/publicKey.pem', 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        """
        Tải khóa riêng tư và khóa công khai từ các tệp .pem.
        Trả về cặp (khóa riêng tư, khóa công khai).
        """
        # Tải khóa riêng tư
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        # Tải khóa công khai
        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk

    def sign(self, message, key):
        """
        Ký dữ liệu bằng khóa riêng tư.
        Args:
            message (str): Tin nhắn cần ký.
            key (ecdsa.SigningKey): Khóa riêng tư dùng để ký.
        Returns:
            bytes: Chữ ký số.
        """
        # Ký dữ liệu bằng khóa riêng tư
        # Encode tin nhắn sang bytes trước khi ký
        return key.sign(message.encode('ascii'))

    def verify(self, message, signature, key):
        """
        Xác minh chữ ký bằng khóa công khai.
        Args:
            message (str): Tin nhắn gốc.
            signature (bytes): Chữ ký cần xác minh.
            key (ecdsa.VerifyingKey): Khóa công khai dùng để xác minh.
        Returns:
            bool: True nếu chữ ký hợp lệ, False nếu không.
        """
        # _ , vk = self.load_keys() # Dòng này trong ảnh có thể gây hiểu nhầm nếu key truyền vào là public key.
                                  # Giả định 'key' trong hàm verify là VerifyingKey.
                                  # Nếu 'key' là một đối tượng public key đã được truyền vào, thì không cần load_keys() ở đây.
                                  # Tuy nhiên, dựa vào hàm trước đó (sign) và cách truyền key trong đoạn code Flask,
                                  # có vẻ như 'key' ở đây là khóa công khai đã được load từ file.
                                  # Để nhất quán với đoạn code Flask trước đó:
        
        # Ở đây, 'key' được truyền vào hàm verify phải là khóa công khai (VerifyingKey)
        vk = key 
        
        try:
            # Xác minh chữ ký. Encode tin nhắn sang bytes trước khi xác minh.
            return vk.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            # Nếu chữ ký không hợp lệ, ecdsa.BadSignatureError sẽ được raise
            return False