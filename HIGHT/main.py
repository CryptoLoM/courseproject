from hight import *


if __name__ == "__main__":
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    plaintext = bytes.fromhex("0011223344556677")
    ciphertext = encrypt_block(plaintext, key)

    print(ciphertext.hex())

    key_path = "keys/keyy.bin"
    input_file = "files/input.txt"
    encrypted_file = "encrypted.bin"
    decrypted_file = "decrypted.txt"

    # generate key if not exists
    if not os.path.exists(key_path):
        with open(key_path, "wb") as f:
            f.write(b"1234567890abcdef")

    print("🔐 Encryption...")
    start_encrypt = time.perf_counter()
    process_file(input_file, encrypted_file, key_path, mode='encrypt')
    end_encrypt = time.perf_counter()
    encrypt_time = end_encrypt - start_encrypt
    print("✅ File encrypted:", encrypted_file)
    print(f"File encryption time with HIGHT cipher: {encrypt_time:.2f} sec")

    print("🔓 Decryption...")
    start_decrypt = time.perf_counter()
    process_file(encrypted_file, decrypted_file, key_path, mode='decrypt')
    end_decrypt = time.perf_counter()
    decrypt_time = end_decrypt - start_decrypt
    print("✅ File decrypted:", decrypted_file)
    print(f"File decryption time with HIGHT cipher {decrypt_time:.2f} sec")

#  or if u want with GUI then comment or delete upper code and uncomment this:
#  run.gui()


