def solve_crackme():
    N = 2630492240428669223384232383096338562137
    e = 65537
    C = 1601640017009476007754247816372425531056

    factors = []
    d_test = 2
    temp_n = N

    while d_test * d_test <= temp_n:
        if temp_n % d_test == 0:
            factors.append(d_test)
            while temp_n % d_test == 0:
                temp_n //= d_test
        d_test += 1
    if temp_n > 1:
        factors.append(temp_n)

    phi = 1
    for p in factors:
        phi *= (p - 1)

    d = pow(e, -1, phi)
    M = pow(C, d, N)

    hex_val = hex(M)[2:]
    if len(hex_val) % 2 != 0:
        hex_val = '0' + hex_val
    password = bytes.fromhex(hex_val).decode('ascii')

    print(password)

if __name__ == "__main__":
    solve_crackme()
