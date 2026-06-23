# Reversing the Key Check — Solution Walkthrough

## 1. Finding the Key Prompt in the Disassembly

While examining the binary in a disassembler (IDA, Ghidra, or similar), I searched for user‑facing strings to locate the key validation logic.
One of the first hits was:

```
Enter key:
```

This indicated that the surrounding function likely performs the actual verification.

Scrolling down the disassembly near this string revealed a loop that computes a value `v7` using each character of the input key.

---

## 2. Extracting the Validation Logic

The decompiled code responsible for checking the key looked like this:

```c
v7 = 0;
for ( i = 0; i < 10; i++ )
{
    v7 = 11 * i + ((input[i] << (i % 3)) ^ v7);
}
if ( v7 != 1337 )
{
    puts("ACCESS DENIED");
}
else
{
    puts("ACCESS GRANTED :)");
}
```

The important parts:

* The key must be exactly **10 characters long**.
* Each character contributes to the running value `v7`.
* The final check is:

```
v7 == 1337
```

So the entire task reduces to:
**Find a 10‑character string such that the loop computes `v7 = 1337`.**

---

## 3. Understanding How `v7` Is Computed

For each index `i` from 0 to 9:

```
v7 = 11*i + ((c << (i % 3)) ^ v7)
```

Where:

* `c` is the ASCII code of the character at position `i`
* `i % 3` cycles through 0,1,2
* `<<` is a left shift
* `^` is XOR

This is a non‑linear recurrence because `v7` depends on the previous `v7` through XOR.

At first glance, brute‑forcing all possible 10‑character strings would be infeasible:

```
(95 printable ASCII characters)^10 ≈ 6e19 combinations
```

So we need something smarter.

---

## 4. Key Insight: The Last Character Can Be Solved Algebraically

Let’s denote:

* `v7_prev` — the value of `v7` after processing the first 9 characters
* `c10` — the ASCII code of the **10th character** (index 9)

The loop iteration for `i = 9` is:

```
v7_final = 11*9 + ((c10 << (9 % 3)) ^ v7_prev)
```

Now compute intermediate values:

* `9 % 3 = 0`
* therefore `c10 << 0 = c10`
* and `11 * 9 = 99`

So the formula becomes:

```
v7_final = 99 + (c10 ^ v7_prev)
```

Since the program requires:

```
v7_final == 1337
```

we get:

```
1337 = 99 + (c10 ^ v7_prev)
c10 ^ v7_prev = 1337 - 99
c10 ^ v7_prev = 1238
```

Solving for the unknown character:

```
c10 = 1238 ^ v7_prev
```

Because XOR is its own inverse, this step is valid.

---

## 5. Why This Means We Don’t Need Full Brute Force

The expression above shows that **for any chosen first 9 characters**, there is exactly one value of `c10` that satisfies the condition.

Thus:

1. Randomly choose 9 characters.
2. Compute `v7_prev`.
3. Compute the required 10th character using:

```
c10 = 1238 ^ v7_prev
```

4. Check if `c10` is a printable ASCII character (`32 ≤ c10 ≤ 126`).
5. If so — we have a valid, human‑readable key.
6. If not — try a different prefix.

This reduces the search space from ~6×10¹⁹ to just a few thousand attempts.

---

## 6. Final Algorithm in Words

* Generate a random 9‑character prefix.
* Run the same loop as the binary for indices 0–8.
* Solve an algebraic XOR equation to determine the required last character.
* If the result is printable, concatenate it to form a valid 10‑character key.
* Otherwise, try again.

This approach guarantees correctness because the last step of the key computation is reversible due to the properties of XOR.

---

## 7. Result

We do **not** brute‑force 10 characters.
We simply:

* brute‑force 9 characters,
* *compute* the 10th one exactly.

This is why the solution runs instantly instead of taking hundreds of years.

keygen

```python
import string
import random

def check(s):
    if len(s) != 10:
        return False
    v7 = 0
    for i in range(10):
        c = s[i] if isinstance(s[i], int) else ord(s[i])
        v7 = 11 * i + ((c << (i % 3)) ^ v7)
    return v7 == 1337

def generate():
    chars = string.printable.strip()
    
    # Жадный подход: фиксируем первые 9 символов, подбираем 10-й
    for _ in range(100_000):
        prefix = [random.choice(chars) for _ in range(9)]
        
        # Вычисляем v7 после 9 итераций
        v7 = 0
        for i in range(9):
            c = ord(prefix[i])
            v7 = 11 * i + ((c << (i % 3)) ^ v7)
        
        # Для i=9: v7_final = 11*9 + ((c << (9%3)) ^ v7) = 99 + (c ^ v7)
        # shift = 9 % 3 = 0, значит c << 0 = c
        # 1337 = 99 + (c ^ v7)  =>  c = (1337 - 99) ^ v7 = 1238 ^ v7
        target_c = 1238 ^ v7
        
        if 32 <= target_c <= 126:  # printable ASCII
            result = ''.join(prefix) + chr(target_c)
            return result
    
    return None

random_result = generate()
print(f"Random: {repr(random_result)}, valid: {check(random_result)}")
```