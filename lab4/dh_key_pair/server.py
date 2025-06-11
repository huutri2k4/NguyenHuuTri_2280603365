from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def generate_dh_parameters():
    """
    Tạo các tham số Diffie-Hellman an toàn.
    """
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def generate_server_key_pair(parameters):
    """
    Tạo cặp khóa riêng tư và công khai Diffie-Hellman cho máy chủ
    dựa trên các tham số đã cho.
    """
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def main():
    """
    Hàm chính để tạo tham số DH, cặp khóa máy chủ và lưu khóa công khai.
    """
    parameters = generate_dh_parameters()
    private_key, public_key = generate_server_key_pair(parameters)

    # Lưu khóa công khai của máy chủ vào file PEM
    with open("server_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    main()