class VigenereCipher:
    def __init__(self, text, keyword):
        self.text = text
        self.keyword = keyword

    def _generate_key(self):
        self.keyword = list(self.keyword)

        if len(self.keyword) == len(self.text):
            return self.keyword
        else:
            for i in range(len(self.text) - len(self.keyword)):
                self.keyword.append(self.keyword[i % len(self.keyword)])

        return (''.join(self.keyword))

    def encrypt(self):
        
        encrypted_message = ""
        key = self._generate_key()

        for i in range(len(self.text)):
            temp = (ord(self.text[i]) + ord(key[i])) % 26
            temp += ord('A')
            encrypted_message += chr(temp)

        return encrypted_message


