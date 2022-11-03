import os

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

class RSA:
    def __init__(self, message: str):
        self.message = message

    def reblocking(self, block_size: int=DEFAULT_BLOCK_SIZE) -> list:
        message_bytes = self.message.encode('ascii')

        blocks = []
        for block in range(0, len(message_bytes), block_size):
            block_to_int = 0
            for i in range(block, min(block + block_size, len(message_bytes))):
                block_to_int += message_bytes[i] * (BYTE_SIZE ** (i % block_size))
            blocks.append(block_to_int)
        
        return blocks

    def handle_blocks(self, blocks: list, message_length: int, block_size: int=DEFAULT_BLOCK_SIZE) -> str:
        message = []

        for block in blocks:
            block_message = []
            for i in range(block_size - 1, -1, -1):
                if len(message) + 1 < message_length:
                    ascii_num = block // (BYTE_SIZE ** i)
                    block = block % (BYTE_SIZE ** i)
                    block_message.insert(0, chr(ascii_num))
            message.extend(block_message)
        return "".join(message)

    def encrypt(self, key: tuple, block_size: int=DEFAULT_BLOCK_SIZE) -> list:
        blocks = self.reblocking(block_size)
        n, e = key
        encrypted_blocks = [pow(block, e, n) for block in blocks]

        return encrypted_blocks

    def decrypt(self, encrypted_blocks: list, message_length: int, key: tuple, block_size: int=DEFAULT_BLOCK_SIZE):
        n, d = key
        decrypted_blocks = [pow(block, d, n) for block in encrypted_blocks]

        return self.handle_blocks(decrypted_blocks, message_length, block_size)
