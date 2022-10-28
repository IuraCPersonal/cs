from ciphers.caesar.CaesarCipher import CaesarCipher
from ciphers.caesar.CaesarCipherWithPermutation import CaesarCipherWithPermutation
from ciphers.caesar.PlayfairCipher import PlayfairCipher
from ciphers.caesar.VigenereCipher import VigenereCipher

class Format:
    __green = '\033[32m'
    __lightgreen = '\033[92m'
    __blue = '\033[34m'
    __red = '\033[31m'
    __pink = '\033[95m'
    __yellow = '\033[93m'

    @staticmethod
    def original(text):
        print(f'{Format.__lightgreen}Original Text: {text}')

    @staticmethod
    def encrypted(text):
        print(f'{Format.__red}{text}')

    @staticmethod
    def br():
        print(f'{Format.__yellow}-----------------------------')

if __name__ == '__main__':
    text = 'cryprographyandsecurity'
    key = 'fcim'

    CC = CaesarCipher(shift=13)
    CCP = CaesarCipherWithPermutation(shift=13)
    PC = PlayfairCipher()
    VP = VigenereCipher(text=text, keyword=key)

    caesar_cipher = CC.encrypt(text)
    caesar_cipher_perm = CCP.encrypt(text=text, keyword=key)
    playfair_cipher = PC.encrypt(text=text, key=key)
    vigenere_cipher = VP.encrypt()

    Format.original(f'{text}')
    Format.encrypted(f'Caesar Cipher: {caesar_cipher}')
    Format.br()

    Format.original(f'{text}')
    Format.encrypted(f'Caesar Cipher With Permutation: {caesar_cipher_perm}')
    Format.br()

    Format.original(f'{text}')
    Format.encrypted(f'Playfair Cipher: {playfair_cipher}')
    Format.br()

    Format.original(f'{text}')
    Format.encrypted(f'Vigenere Cipher: {vigenere_cipher}')
    Format.br()



