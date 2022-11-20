class CaesarCipher:
    def __init__(self, shift=9):
        self.shift = shift % 26

    def encrypt(self, msg):
        text = ''

        for char in msg:
            if char.isupper():
                text += chr((ord(char) + self.shift - 65) % 26 + 65)
            else:
                text += chr((ord(char) + self.shift - 97) % 26 + 97)

        return text

    def decrypt(self, msg):
        text = ''

        for char in msg:
            if char.isupper():
                text += chr((ord(char) + 26 - self.shift - 65) % 26 + 65)
            else:
                text += chr((ord(char) + 26 - self.shift - 97) % 26 + 97)

        return text