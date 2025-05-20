from hight import *


if __name__ == "__main__":
    key_path = "keys/keyy.bin"
    input_file = "files/SCrypto.pdf"
    encrypted_file = "SCrypto.pdf.bin"
    decrypted_file = "decrypted_SCrypto.pdf"

    # generate key if not exists
    if not os.path.exists(key_path):
        with open(key_path, "wb") as f:
            f.write(b"1234567890abcdef")

    print("🔐 Шифрування...")
    start_encrypt = time.perf_counter()
    process_file(input_file, encrypted_file, key_path, mode='encrypt')
    end_encrypt = time.perf_counter()
    encrypt_time = end_encrypt - start_encrypt
    print("✅ Файл зашифровано:", encrypted_file)
    print(f"Час шифрування файлу шифром HIGHT: {encrypt_time:.2f} секунд")

    print("🔓 Дешифрування...")
    start_decrypt = time.perf_counter()
    process_file(encrypted_file, decrypted_file, key_path, mode='decrypt')
    end_decrypt = time.perf_counter()
    decrypt_time = end_decrypt - start_decrypt
    print("✅ Файл розшифровано:", decrypted_file)
    print(f"Час розшифрування файлу шифром HIGHT: {decrypt_time:.2f} секунд")

#  or if u want with GUI then comment upper code and uncomment this:
#  run.gui()


