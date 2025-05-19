from hight import *


def process_file(input_file, output_file, key_file, mode):
    BUFFER_SIZE = 64 * 1024

    with open(key_file, 'rb') as f:
        key = f.read()
    if len(key) != 16:
        raise ValueError("Ключ повинен мати 16 байт.")

    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        if mode == 'encrypt':
            original_size = os.path.getsize(input_file)
            fout.write(struct.pack('<Q', original_size))  # записуємо розмір

        elif mode == 'decrypt':
            size_data = fin.read(8)
            original_size = struct.unpack('<Q', size_data)[0]

        total_written = 0
        while True:
            chunk = fin.read(BUFFER_SIZE)
            if not chunk:
                break

            # Розбиваємо chunk на 8-байтні блоки
            blocks = [chunk[i:i+8] for i in range(0, len(chunk), 8)]
            for block in blocks:
                if len(block) < 8:
                    block = block.ljust(8, b'\0')  # паддінг
                if mode == 'encrypt':
                    fout.write(encrypt_block(block, key))
                    total_written += 8
                else:
                    decrypted_block = decrypt_block(block, key)
                    # Відкладене обрізання паддінгу
                    if total_written + 8 <= original_size:
                        fout.write(decrypted_block)
                        total_written += 8
                    else:
                        to_write = original_size - total_written
                        fout.write(decrypted_block[:to_write])
                        total_written += to_write

with open("key.bin", "wb") as f:
    f.write(b"1234567890abcdef")  # 16 байт


def decrypt_data(fin, fout, key, original_size):
    total_written = 0
    while True:
        chunk = fin.read(BUFFER_SIZE)  # delete this
        if not chunk:
            break
    #  if len(block) < 8:
        # block = block.ljust(8, b'\0')
        # Замість читання по частинах (chunk), читається весь залишок файлу одразу (це безпечно, бо BUFFER_SIZE вже обмежував під час шифрування).

        blocks = [chunk[i:i+8] for i in range(0, len(chunk), 8)]
        for block in blocks:
            decrypted_block = decrypt_block(block, key)
            if total_written + 8 <= original_size:
                fout.write(decrypted_block)
                total_written += 8
            else:
                to_write = original_size - total_written
                fout.write(decrypted_block[:to_write])
                total_written += to_write