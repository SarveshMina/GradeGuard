from Crypto.Cipher import AES
import binascii

# 1) Your 16-byte (128-bit) AES key in hex:
key_hex = "01189998819991197253FFFFFFFFFFFF"

# 2) The ciphertext from the lab (all hex). Remove line breaks:
cipher_hex = """
F68E619820F41B0705759AC116193829098872E175F0859012F6F88DF2246CB7CE685
26A85380F9AF5D6A2965A7CFD3A7691B998F672581BDE316F8AA243B3B2173F3C4A05
E3B51932D194FC02C93AC92A4FEB6C3B666B4EAF1E275520F886D7A63B47E128C478D
838EA699690777FE11ABB9280F9510A9D45125CE29741E04C7C643D72487E38897101
78266AF0DD5C81C0FFC6750F968269F151B23039BD2057D672D8F4D9B5D3C592285E3
E7B80E1
""".replace("\n", "")

# Convert hex to raw bytes:
key = binascii.unhexlify(key_hex)
ciphertext = binascii.unhexlify(cipher_hex)

# 3) Create AES object (ECB mode assumed unless specified otherwise)
cipher = AES.new(key, AES.MODE_ECB)

# 4) Decrypt:
plaintext = cipher.decrypt(ciphertext)

print("Plaintext bytes:")
print(plaintext)

# If it looks like ASCII text, do:
try:
    print("\nDecoded as ASCII/UTF-8:")
    print(plaintext.decode('utf-8'))
except UnicodeDecodeError:
    print("\n(Plaintext not valid UTF-8 or may need another encoding.)")
