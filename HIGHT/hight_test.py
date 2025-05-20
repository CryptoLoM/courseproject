import unittest
from hight import *


class TestHIGHTCipher(unittest.TestCase):
    test_vectors = [
        {
            "key": "00112233445566778899aabbccddeeff",
            "plaintext": "0011223344556677",
            "ciphertext": "d19d54664d642492",
        },
        {
            "key": "000102030405060708090a0b0c0d0e0f",
            "plaintext": "0001020304050607",
            "ciphertext": "5b077d9bdbdf90f0",
        },
        {
            "key": "ffffffffffffffffffffffffffffffff",
            "plaintext": "0000000000000000",
            "ciphertext": "e54d0d61f9ce9f8a",
        },
        {
            "key": "00000000000000000000000000000000",
            "plaintext": "ffffffffffffffff",
            "ciphertext": "5bc2de8ffb5e084d",
        },
        {
            "key": "01010101010101010101010101010101",
            "plaintext": "0202020202020202",
            "ciphertext": "b7ffec0948e06f3f",
        },
    ]

    for i, vector in enumerate(test_vectors):
        pt = bytes.fromhex(vector["plaintext"])
        key = bytes.fromhex(vector["key"])
        expected = vector["ciphertext"]
        result = encrypt_block(pt, key).hex()
        print(f"Test {i + 1}: {'OK' if result == expected else 'FAIL'} | Result: {result}")

    def test_padding_and_unpadding(self):
        # Test that encryption/decryption handles padding correctly
        key = b"1234567890abcdef"
        plaintext = b"12345"  # Not a full 8-byte block
        padded = plaintext.ljust(8, b'\0')
        ciphertext = encrypt_block(padded, key)
        decrypted = decrypt_block(ciphertext, key)
        unpadded = decrypted.rstrip(b'\0')
        self.assertEqual(unpadded, plaintext)

    def test_all_zero_key_and_plaintext(self):
        key = bytes([0] * 16)
        plaintext = bytes([0] * 8)
        ciphertext = encrypt_block(plaintext, key)
        decrypted = decrypt_block(ciphertext, key)
        self.assertEqual(decrypted, plaintext)

    def test_randomized_blocks(self):
        import os
        key = os.urandom(16)
        for _ in range(10):
            plaintext = os.urandom(8)
            ciphertext = encrypt_block(plaintext, key)
            decrypted = decrypt_block(ciphertext, key)
            self.assertEqual(decrypted, plaintext)

    def test_round_trip(self):
        key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
        plaintext = bytes.fromhex("0001020304050607")

        cipher = encrypt_block(plaintext, key)
        print("Ciphertext:", cipher.hex())

        decrypted = decrypt_block(cipher, key)
        print("Decrypted :", decrypted.hex())

        self.assertEqual(decrypted, plaintext)

    def test_hight_cipher(self):
        key = bytes.fromhex('00112233445566778899aabbccddeeff')
        plaintext = bytes.fromhex('0011223344556677')
        ciphertext = encrypt_block(plaintext, key)
        decrypted = decrypt_block(ciphertext, key)
        self.assertEqual(decrypted, plaintext)

    def test_double_encryption_and_decryption(self):
        key = bytes.fromhex('0123456789abcdeffedcba9876543210')
        plaintext = bytes.fromhex('deadbeefcafebabe')
        encrypted_once = encrypt_block(plaintext, key)
        encrypted_twice = encrypt_block(encrypted_once, key)
        decrypted_once = decrypt_block(encrypted_twice, key)
        decrypted_twice = decrypt_block(decrypted_once, key)
        self.assertEqual(decrypted_twice, plaintext)



if __name__ == '__main__':
    unittest.main()
