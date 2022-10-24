import random
import cryptography as cs
from rabin_miller import RabinMiller 


class RSA_KEY_GEN:
    @staticmethod
    def key_gen(key_size: int=1024) -> list:
        # Generate prime p
        p = RabinMiller.generate_large_prime(key_size)

        # Generate prime q
        q = RabinMiller.generate_large_prime(key_size)

        n = p * q

        while True:
            e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
            if cs.gcd(e, (p - 1) * (q - 1)) == 1:
                break

        d = cs.find_mod_inverse(e, (p - 1) * (q - 1))

        public_key = (n, e)
        private_key = (n, d)

        return [public_key, private_key]