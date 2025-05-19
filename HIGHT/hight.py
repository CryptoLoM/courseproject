# HIGHT Block Cipher (64-bit block, 128-bit key)
# Full implementation: encryption and decryption with file interface
import os
import argparse
import struct
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

# === LFSR-Based Constant Generation (δ₀..δ₁₂₇) ===
def constant_generation():
    s = [0, 1, 0, 1, 1, 0, 1]  # s₀..s₆
    deltas = []

    def to_byte(bits):
        return sum(b << i for i, b in enumerate(bits))

    deltas.append(to_byte(s[::-1]))
    for _ in range(127):
        new_bit = s[2] ^ s[6]  # sᵢ₊₆ ← s₂ ⊕ s₆
        s = s[1:] + [new_bit]
        deltas.append(to_byte(s[::-1]))
    return deltas

# === Whitening Key Generation ===
def whitening_key_generation(mk):
    assert len(mk) == 16
    return [mk[i + 12] if i <= 3 else mk[i - 4] for i in range(8)]

# === Subkey Generation ===
def subkey_generation(mk):
    assert len(mk) == 16
    deltas = constant_generation()
    sk = [(mk[i % 8] + deltas[i]) & 0xFF for i in range(128)]
    return sk

# === DELTA (precomputed constants) replaced with actual constant generation ===
DELTA = constant_generation()

def rol(x, n):
    return ((x << n) & 0xFF) | (x >> (8 - n))

def ror(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xFF

# === F0 and F1 functions from specification ===
def F0(x):
    return rol(x, 1) ^ rol(x, 2) ^ rol(x, 7)  # x << 1 ⊕ x << 2 ⊕ x << 7

def F1(x):
    return rol(x, 3) ^ rol(x, 4) ^ rol(x, 6) # x << 3 ⊕ x << 4 ⊕ x << 6

def generate_round_keys(master_key: bytes):
    return subkey_generation(list(master_key))

def whitening(input_block, keys):
    x = input_block[:]
    x[0] ^= keys[0]
    x[2] ^= keys[1]
    x[4] ^= keys[2]
    x[6] ^= keys[3]
    return x

def whitening_inverse(output_block, keys):
    x = output_block[:]
    x[0] ^= keys[0]
    x[2] ^= keys[1]
    x[4] ^= keys[2]
    x[6] ^= keys[3]
    return x

def encrypt_block(block: bytes, key: bytes) -> bytes:
    wk = whitening_key_generation(key)
    rk = generate_round_keys(key)
    x = list(block)
    x = whitening(x, wk[:4])
    for i in range(32):
        x_new = x[:]
        x_new[1] = (x[1] + (F1(x[0]) ^ rk[4 * i + 3])) & 0xFF # X1 ← X1 + (F1(X0) ⊕ SK4i+3)
        x_new[3] = (x[3] ^ ((F0(x[2]) + rk[4 * i + 2]) & 0xFF)) & 0xFF  # X3 ← X3 ⊕ (F0(X2) + SK4i+2)
        x_new[5] = (x[5] + (F1(x[4]) ^ rk[4 * i + 1])) & 0xFF  # X5 ← X5 + (F1(X4) ⊕ SK4i+1)
        x_new[7] = (x[7] ^ ((F0(x[6]) + rk[4 * i + 0]) & 0xFF)) & 0xFF # X7 ← X7 ⊕ (F0(X6) + SK4i)
        x = x_new
    x = whitening(x, wk[4:])
    return bytes(x)

    x = whitening(x, wk[4:])
    return bytes(x)

def decrypt_block(block: bytes, key: bytes) -> bytes:
    wk = whitening_key_generation(key)
    rk = generate_round_keys(key)
    x = list(block)
    x = whitening_inverse(x, wk[4:])
    for i in reversed(range(32)):
        x_new = x[:]
        # X1 ← X1 - (F1(X0) ⊕ SK4i+3)
        x_new[1] = (x[1] - (F1(x[0]) ^ rk[4 * i + 3])) & 0xFF
        # X3 ← X3 ⊕ (F0(X2) + SK4i+2)
        x_new[3] = (x[3] ^ ((F0(x[2]) + rk[4 * i + 2]) & 0xFF)) & 0xFF
        # X5 ← X5 - (F1(X4) ⊕ SK4i+1)
        x_new[5] = (x[5] - (F1(x[4]) ^ rk[4 * i + 1])) & 0xFF
        # X7 ← X7 ⊕ (F0(X6) + SK4i)
        x_new[7] = (x[7] ^ ((F0(x[6]) + rk[4 * i + 0]) & 0xFF)) & 0xFF
        x = x_new

    x = whitening_inverse(x, wk[:4])
    return bytes(x)


BUFFER_SIZE = 5 * 1024 * 1024 * 1024   # 5GB

def encrypt_data(fin, fout, key):
    total_written = 0
         # Розбиваємо chunk на 8-байтні блоки
    blocks = [chunk[i:i + 8] for i in range(0, len(chunk), 8)]
    for block in blocks:
        if len(block) < 8:
            block = block.ljust(8, b'\0')
        fout.write(encrypt_block(block, key))
        total_written += 8

def decrypt_data(fin, fout, key, original_size):
    total_written = 0
    encrypted_data = fin.read()

    # ➤ Перевірка на відповідність режиму ECB: довжина має бути кратна 8
    if len(encrypted_data) % 8 != 0:
        raise ValueError("Помилка: довжина зашифрованих даних не кратна 8 байтам (розмір блоку в режимі ECB).")

    blocks = [encrypted_data[i:i+8] for i in range(0, len(encrypted_data), 8)]
    for block in blocks:
        decrypted_block = decrypt_block(block, key)
        if total_written + 8 <= original_size:
            fout.write(decrypted_block)
            total_written += 8
        else:
            # Запис лише необхідної кількості байт, якщо останній блок містить padding
            to_write = original_size - total_written
            fout.write(decrypted_block[:to_write])
            total_written += to_write

def process_file(input_file, output_file, key_file, mode):
    with open(key_file, 'rb') as f:
        key = f.read()


    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        if mode == 'encrypt':
            original_size = os.path.getsize(input_file)
            fout.write(struct.pack('<Q', original_size))
            encrypt_data(fin, fout, key)

        elif mode == 'decrypt':
            size_data = fin.read(8)
            original_size = struct.unpack('<Q', size_data)[0]
            decrypt_data(fin, fout, key, original_size)

with open("key.bin", "wb") as f:
    f.write(b"1234567890abcdef")  # 16 байт
