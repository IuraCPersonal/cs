import string


class CaesarCipherWithPermutation:
    def __init__(self, shift=8):
        self.shift = shift

    def __alphabet_permutation(self, keyword):
        alphabet = string.ascii_lowercase

        s = alphabet.translate({ord(c): None for c in keyword.lower()})
        s = keyword.lower() + s

        return s

    def encrypt(self, text, keyword='FAF'):
        new_alphabet = self.__alphabet_permutation(keyword)
        cipher_text = ''

        for index, c in enumerate(text):
            cipher_text += new_alphabet[(new_alphabet.find(c) + self.shift) % len(new_alphabet)]

        return cipher_text
