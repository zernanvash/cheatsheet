import random
import string


def generate_key():
    charset = string.ascii_letters + string.digits + string.punctuation
    while True:
        k = [random.choice(charset) for _ in range(6)]
        current_sum = sum(ord(c) for c in k[:5]) - ord(k[5])
        target_k6 = (353 - current_sum) % 256
        if 32 <= target_k6 <= 126:
            k6_char = chr(target_k6)
            k.append(k6_char)
            k.extend([random.choice(charset) for _ in range(3)])
            return "".join(k)

for i in range(5):
    print(f"Key {i + 1}: {generate_key()}")