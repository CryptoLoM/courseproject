import unittest
from hight import *

class TestHIGHTCipher(unittest.TestCase):

    def test_round_trip(self):
        key = b"1234567890abcdef"  # 16 байт
        plaintext = b"ABCDEFGH"     # 8 байт

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

    def test_key_length(self):
        with self.assertRaises(AssertionError):
            encrypt_block(b'12345678', b'123456789012345')

        with self.assertRaises(AssertionError):
            encrypt_block(b'12345678', b'12345678901234567890')

    def test_block_length(self):
        with self.assertRaises(AssertionError):
            encrypt_block(b'1234567', b'1234567890123456')

if __name__ == '__main__':
    unittest.main()
