class CaesarCipher:
    @staticmethod
    def encrypt(msg, shift=9):
        text = ''

        for char in msg:
            if char.isupper():
                text += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                text += chr((ord(char) + shift - 97) % 26 + 97)

        return text


    @staticmethod
    def decrypt(msg):
        text = ''

        for char in msg:
            if char.isupper():
                text += chr((ord(char) + 26 - shift - 65) % 26 + 65)
            else:
                text += chr((ord(char) + 26 - shift - 97) % 26 + 97)

        return 