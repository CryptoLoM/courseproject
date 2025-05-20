import unittest
from hight import *

class TestHIGHTCipher(unittest.TestCase):

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
        key = b"1234567890abcdef"
        plaintext = b"ABCDEFGH"

        cipher = encrypt_block(plaintext, key)
        decrypted = decrypt_block(cipher, key)
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
