import string


class CaesarCipherWithPermutation:
    def __init__(self, shift=8):
        self.shift = shift

    def __alphabet_permutation(self, keyword):
        alphabet = string.ascii_uppercase

        alphabet_with_permutation = ''.join(sorted(set(keyword), key=keyword.index))

    def encrypt(self, text):
        pass

        
