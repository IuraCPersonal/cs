from CaesarCipher import CaesarCipher

if __name__ == '__main__':
    cipher = CaesarCipher(shift=28)

    print(cipher.encrypt('Lorem ipsum frog the fog.'))
    print(cipher.decrypt('CDEF'))
