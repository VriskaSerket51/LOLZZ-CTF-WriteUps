# KittyCrypt

There is example input, output and flag_output with encrypt code. Since we know pair of input and output, we can know what is the key and find the flag with that key.


```python
import binascii

# Go 코드 CharSet의 역매핑 (이모지 → 16진수 한 글자)
CAT_TO_HEX = {
    "🐱": "0", "🐈": "1", "😸": "2", "😹": "3",
    "😺": "4", "😻": "5", "😼": "6", "😽": "7",
    "😾": "8", "😿": "9", "🙀": "A", "🐱‍👤": "B",
    "🐱‍🏍": "C", "🐱‍💻": "D", "🐱‍👓": "E", "🐱‍🚀": "F",
}

def cat_to_hex_str(cat_cipher: str) -> str:
    i = 0
    hex_chars = []
    sorted_keys = sorted(CAT_TO_HEX.keys(), key=len, reverse=True)

    while i < len(cat_cipher):
        for k in sorted_keys:
            if cat_cipher.startswith(k, i):
                hex_chars.append(CAT_TO_HEX[k])
                i += len(k)
                break
        else:
            raise ValueError(f"Unknown cat emoji at pos={i} -> {cat_cipher[i:i+5]}")
    return "".join(hex_chars)

def hex_str_to_keyed_text(hex_str: str) -> str:
    raw = binascii.unhexlify(hex_str)
    return raw.decode('utf-8', errors='replace')

def recover_key(plaintext: str, keyed_text: str) -> list:
    return [ord(k) - ord(p) for p, k in zip(plaintext, keyed_text)]

def decrypt_cat_cipher(cat_cipher: str, keys: list) -> str:
    hex_str = cat_to_hex_str(cat_cipher)
    keyed_text = hex_str_to_keyed_text(hex_str)

    decrypted = []
    for i, ch in enumerate(keyed_text):
        decrypted.append(chr(ord(ch) - keys[i]))
    return "".join(decrypted)

def main():
    with open("example_input.txt", "r", encoding="utf-8") as f:
        example_plain = f.read()
    with open("example_output.txt", "r", encoding="utf-8") as f:
        example_cipher = f.read()

    ex_hex_str = cat_to_hex_str(example_cipher)
    ex_keyed_text = hex_str_to_keyed_text(ex_hex_str)
    keys = recover_key(example_plain, ex_keyed_text)

    with open("flag_output.txt", "r", encoding="utf-8") as f:
        flag_cipher = f.read()

    flag_plain = decrypt_cat_cipher(flag_cipher, keys)
    print("[+] Flag:")
    print(flag_plain)

if __name__ == "__main__":
    main()
```


flag is: **irisctf{s0m371m3s_bY735_4r3n7_wh47_y0u_3xp3c7}**