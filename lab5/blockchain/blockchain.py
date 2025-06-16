import hashlib
import time
from block import Block  # Đã sửa lỗi thừa 'from'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Tạo khối genesis (khối đầu tiên)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        # Tạo một khối mới với các thông tin cung cấp
        block = Block(len(self.chain) + 1, previous_hash, time.time(), self.current_transactions, proof)
        self.current_transactions = []  # Đặt lại danh sách giao dịch hiện tại sau khi thêm vào khối
        self.chain.append(block)  # Thêm khối mới vào chuỗi
        return block

    def get_previous_block(self):
        # Trả về khối cuối cùng trong chuỗi
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        # Thuật toán Proof of Work để tìm ra một "proof" hợp lệ
        new_proof = 1
        check_proof = False
        while not check_proof:
            # Tính toán hash của một số được mã hóa dựa trên new_proof và previous_proof
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Kiểm tra xem hash có bắt đầu bằng '0000' không (độ khó)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        # Thêm một giao dịch mới vào danh sách giao dịch hiện tại
        self.current_transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        # Trả về index của khối tiếp theo sẽ được tạo
        return self.get_previous_block().index + 1

    def is_chain_valid(self, chain):
        # Kiểm tra tính hợp lệ của toàn bộ chuỗi
        previous_block = chain[0]  # Bắt đầu từ khối genesis
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]

            # 1. Kiểm tra hash của khối hiện tại có khớp với previous_hash trong khối tiếp theo không
            if block.previous_hash != previous_block.hash:
                return False

            # 2. Kiểm tra Proof of Work của khối hiện tại
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            
            if hash_operation[:4] != '0000': # Sửa lại để kiểm tra nếu PoW KHÔNG hợp lệ
                return False # Trả về False nếu PoW không đúng

            previous_block = block  # Di chuyển đến khối tiếp theo
            block_index += 1
        return True # Nếu duyệt qua hết mà không có lỗi, chuỗi hợp lệ