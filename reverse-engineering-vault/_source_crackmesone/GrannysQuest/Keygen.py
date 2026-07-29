import struct

def day1():
    return "00700900"

def day2():
    s = "Dlyyov#Dsvvoh#Fmornrgvw"
    result = []
    for c in s:
        if c < 'A':
            result.append('-')
        elif c <= 'Z':
            result.append(chr(ord('Z') - ord(c) + ord('A')))
        else:
            result.append(chr(ord('z') - ord(c) + ord('a')))
    return ''.join(result)

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def day3(name):
    return ''.join(str(fib(ord(c) - ord('a'))) for c in name.lower()[:8])

def day4_launch():
    return "003-00005-003"

def day4_coords():
    return "40.8214,14.4262"

def day4_verify(name):
    v8 = (0x309 * len(name)) ^ 0x8000000000000000
    if v8 >= 2 ** 63:
        v8 -= 2 ** 64
    return str(v8)

if __name__ == "__main__":
    print("=== GRANNY'S QUEST KEYGEN ===\n")
    print(f"Day 1 (birthday):     {day1()}")
    print(f"Day 2 (manufacturer): {day2()}")
    name = input("\nEnter your name (max 8 chars): ").strip()[:8]
    print(f"Day 3 (number code):  {day3(name)}")
    print(f"\nDay 4 launch code:    {day4_launch()}")
    print(f"Day 4 coordinates:    {day4_coords()}")
    print(f"Day 4 verification:   {day4_verify(name)}")