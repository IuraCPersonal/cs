class CaesarCipher:
    def __init__(self, shift=9):
        self.shift = shift % 26

    def encrypt(self, msg):
        self.text = ''

        for char in msg:
            if char.isupper():
                self.text += chr((ord(char) + self.shift - 65) % 26 + 65)
            else:
                self.text += chr((ord(char) + self.shift - 97) % 26 + 97)

        return self.text

    def decrypt(self, msg):
        self.text = ''

        for char in msg:
            if char.isupper():
                self.text += chr((ord(char) + 26 - self.shift - 65) % 26 + 65)
            else:
                self.text += chr((ord(char) + 26 - self.shift - 97) % 26 + 97)

        return self.text
    
    def __str__(self):
        return self.text
