from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from sha256 import SHA256

import sys
import hashlib
import argparse

sys.path.append('../../cs')


dummy_datastore = {}


class DigitalSignature:
    # Preprocess the message, if needed.
    @staticmethod
    def take_input():
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-s",
            "--string",
            dest="input_string",
            default="Hello World!! Welcome to Cryptography",
            help="Hash the string",
        )

        parser.add_argument(
            "-f",
            "--file",
            dest="input_file",
            help="Hash contents of a file"
        )

        args = parser.parse_args()
        input_string = args.input_string

        # hash input should be a bytestring
        if args.input_file:
            with open(args.input_file, "rb") as f:
                hash_input = f.read()
        else:
            hash_input = bytes(input_string, "utf-8")

        return hash_input

    @staticmethod
    def assymetric_encryption(msg):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        encrypted = public_key.encrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted, private_key

    @staticmethod
    def assymetric_decryption(encrypted_message, private_key):
        original_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return original_message

    @staticmethod
    def digital_signature_check(original_message, decrypted_message):
        if SHA256(original_message).hash == decrypted_message:
            print("STATUS: OK. HASHES ARE THE SAME")

    @staticmethod
    def save_to_datastore(key, input_string):
        dummy_datastore[key] = SHA256(input_string).hash


if __name__ == '__main__':
    # Take the user input message.
    msg = DigitalSignature.take_input()

    # Get a digest of it via hashing.
    hashed_input = SHA256(msg).hash

    # Encrypted message.
    enc_msg, private_key = DigitalSignature.assymetric_encryption(
        hashed_input.encode())
    dcp_msg = DigitalSignature.assymetric_decryption(
        enc_msg, private_key).decode()

    DigitalSignature.digital_signature_check(msg, dcp_msg)
