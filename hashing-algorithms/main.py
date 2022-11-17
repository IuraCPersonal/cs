import sys
import argparse
import unittest

sys.path.append('../../cs')

from sha256 import SHA256
from cryptography.fernet import Fernet


# class SHA256HashTest(unittest.TestCase):
#     """
#     Test class for the SHA256 class. Inherits the TestCase class from unittest
#     """
#     def test_match_hashes(self) -> None:
#         import hashlib

#         test_case = bytes("Test String", "utf-8")

#         self.assertEqual(SHA256(test_case).hash, hashlib.sha256(test_case).hexdigest())


def main() -> None:
    unittest.main()

    import doctest

    doctest.testmod()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--string",
        dest="input_string",
        default="Hello World!! Welcome to Cryptography",
        help="Hash the string",
    )
    parser.add_argument(
        "-f", "--file", dest="input_file", help="Hash contents of a file"
    )

    args = parser.parse_args()

    input_string = args.input_string

    # hash input should be a bytestring
    if args.input_file:
        with open(args.input_file, "rb") as f:
            hash_input = f.read()
    else:
        hash_input = bytes(input_string, "utf-8")

    hashed_input = SHA256(hash_input).hash


if __name__ == "__main__":
    main()