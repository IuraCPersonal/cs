import struct

class SHA256:
    def __init__(self, data: bytes) -> None:
        self.data = data

        # Initialize hash values.
        # (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):
        self.hashes = [
            0x6a09e667, 0xbb67ae85,
            0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c,
            0x1f83d9ab, 0x5be0cd19
        ]

        # Initialize array of round constants.
        # (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311):
        self.constants = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        self.hashing()

    # Preprocessing
    @staticmethod
    def preprocessing(data: bytes) -> bytes:
        padding = b"\x80" + (b"\x00" * (63 - (len(data) + 8) % 64))
        big_endian_integer = struct.pack(">Q", (len(data) * 8))

        return data + padding + big_endian_integer

    def right_rotate(self, value: int, rotations: int) -> int:
        """
        Right rotate a given unsigned number by a certain amount of rotations
        """
        return 0xFFFFFFFF & (value << (32 - rotations)) | (value >> rotations)     


    def hashing(self) -> None:
        # Compute the preprocessed data.
        self.preprocessed_data = self.preprocessing(self.data)
        self.blocks = []

        # Convert the data in 64 bytes blocks.
        for block_split in range(0, len(self.preprocessed_data), 64):
            self.blocks.append(self.preprocessed_data[block_split:block_split+64])

        # Convert the blocks into lists of 64 byte integers.
        for block in self.blocks:
            # Copy block into first 16 words w[0..15] of the message schedule array.
            words = list(struct.unpack(">16L", block))
            
            # The initial values in w[0..63] don't matter, so many implementations zero them here.
            words += [0] * 48

            # Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array:
            for i in range(16, 64):
                s0 = (
                    self.right_rotate(words[i - 15], 7) ^ self.right_rotate(words[i - 15], 18) ^ (words[i - 15] >> 3)
                )

                s1 = (
                    self.right_rotate(words[i - 2], 17) ^ self.right_rotate(words[i - 2], 19) ^ (words[i - 2] >> 10)
                )

                words[i] = (words[i - 16] + s0 + words[i - 7] + s1) % 0x100000000

            # Initialize working variables to current hash value.
            a, b, c, d, e, f, g, h = self.hashes

            # Compression function main loop.
            for index in range(0, 64):
                s1 = self.right_rotate(e, 6) ^ self.right_rotate(e, 11) ^ self.right_rotate(e, 25)
                ch = (e & f) ^ ((~e & (0xFFFFFFFF)) & g)
                temp1 = (
                    h + s1 + ch + self.constants[index] + words[index]
                ) % 0x100000000
                s0 = self.right_rotate(a, 2) ^ self.right_rotate(a, 13) ^ self.right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (s0 + maj) % 0x100000000

                h = g
                g = f
                f = e
                e = ((d + temp1) % 0x100000000)
                d = c
                c = b
                b = a
                a = ((temp1 + temp2) % 0x100000000)

            mutated_hash_values = [a, b, c, d, e, f, g, h]

            # Add the compressed chunk to the current hash value.
            self.hashes = [
                ((element + mutated_hash_values[index]) % 0x100000000)
                for index, element in enumerate(self.hashes)
            ]
        
        # Produce the final hash value (big-endian)
        self.hash = "".join([hex(value)[2:].zfill(8) for value in self.hashes])