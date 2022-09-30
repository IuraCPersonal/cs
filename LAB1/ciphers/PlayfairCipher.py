
class PlayfairCipher:
    def __init__(self, text):
        self.text = text

    def __to_lower_case(self, text):
        return text.lower()

    def __remove_white_space(self, text):
        return text.strip()

    def get_diagraph(self):
        diagraph = list()
        group = 0

        for i in range(2, len(self.text), 2):
            diagraph.append(self.text[group:i])

            group = i

        diagraph.append(self.text[group:])
        return diagraph

    def filler_letter(self):
        k = len(self.text)

        if k % 2 == 0:
            for i in range(0, k, 2):
                if self.text[i] == self.text[i+1]:
                    new_word = self.text[0:i+1] + str('x') + self.text[i+1:]
                    new_word = self.filler_letter(new_word)
                    break
                else:
                    new_word = self.text
        else:
            for i in range(0, k-1, 2):
                if self.text[i] == text[i+1]:
                    new_word = text[0:i+1] + str('x') + self.text[i+1:]
                    new_word = self.filler_letter(new_word)
                    break
                else:
                    new_word = text
        return new_word

    
    def generate_key_table(self, word):
        list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        key_letters = []

        for i in word:
            if i not in key_letters:
                key_letters.append(i)

        comp_elements = []
        for i in key_letters:
            if i not in comp_elements:
                comp_elements.append(i)

        matrix = []

        while comp_elements != []:
            matrix.append(comp_elements[:5])
            comp_elements = comp_elements[5:]

        return matrix

    def search(self, matrix, element):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if (matrix[i][j] == element):
                    return i, j

    def encrypt_row(self, matrix, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1c == 4:
            char1 = matrix[e1r][0]
        else:
            char1 = matrix[e1r][e1c+1]

        char2 = ''
        if e2c == 4:
            char2 = matrix[e2r][0]
        else:
            char2 = matrix[e2r][e2c+1]

        return char1, char2

    def encrypt_column(self, matrix, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1c == 4:
            char1 = matrix[0][e1r]
        else:
            char1 = matrix[e1r+1][e1c]

        char2 = ''
        if e2c == 4:
            char2 = matrix[0][e2c]
        else:
            char2 = matrix[e2r+1][e2c]

        return char1, char2

    def encrypt_rectangule(self, matrix, e1r, e1c, e2r, e2c):
        return matrix[e1r][e2c], matrix[e2r][e1c]

    def encrypt(self, matrix, plainlist):
        cipher_text = []

        for i in range(0, len(plainlist)):
            c1, c2 = 0, 0
            elm_1x, elm_1y = self.search(Matrix, plainlist[i][0])
            elm_2x, elm_2y = self.search(Matrix, plainlist[i][1])

            if elm_1x == elm_2x:
                c1, c2 = self.encrypt_row(Matrix, elm_1x, elm_1y, elm_2x, elm_2y)
            elif elm_1y == elm_2y:
                c1, c2 = self.encrypt_column(Matrix, elm_1x, elm_1y, elm_2x, elm_2y)
            else:
                c1, c2 = self.encrypt_rectangule(Matrix, elm_1x, elm_1y, elm_2x, elm_2y)

            cipher = c1 + c2
            cipher_text.append(cipher)

        return cipher_text
