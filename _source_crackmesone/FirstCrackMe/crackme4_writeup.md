# crackme 4.exe Writeup

## Summary

- Target: `/Users/singularity/Downloads/crackme 4.exe`
- SHA-256: `dead29f6b77611aacf0467139236c0ddc6fb422bfa0422721003c9f19c46ca1a`
- Format: PE32+ Windows console executable, x86-64
- Tooling: IDA Pro MCP, `strings`, `objdump`, Wine attempted for runtime validation
- Result: password is `simba123`

## Triage

IDA loaded the program as a small native PE executable, not as a managed .NET assembly. The prompt metadata says C#/.NET, but the binary imports `msvcrt.dll` and `KERNEL32.dll`, has MinGW CRT startup code, and `objdump` reports an empty CLR Runtime Header data directory.

Important strings:

```text
Enter password:
simba123
CORRECT!
WRONG!
%99s
```

## Static Analysis

IDA identifies the main validation routine at `0x140001490` (`main`). The function:

1. Prints `Enter password: `
2. Reads user input into a global buffer with `scanf("%99s", input)`
3. Compares the input with the static password string at `0x140003011`
4. Prints `CORRECT!` if the comparison succeeds, otherwise `WRONG!`

Relevant IDA findings:

- `0x140001490`: `main`
- `0x140003011`: password string `simba123`
- `0x14000301a`: success string `CORRECT!`
- `0x140003023`: failure string `WRONG!`
- imported comparison routine: `strcmp`

The core logic is equivalent to:

```c
printf("Enter password: ");
scanf("%99s", input);

if (strcmp(input, "simba123") == 0) {
    puts("CORRECT!");
} else {
    puts("WRONG!");
}
```

## Validation

Static validation is direct: IDA shows the static expected string `simba123` passed to `strcmp` against the input buffer.

I also attempted to run the program under Wine with:

```bash
printf 'simba123\n' | wine '/Users/singularity/Downloads/crackme 4.exe'
```

Wine crashed before producing the program output in this macOS environment, so runtime validation could not be completed here. The recovered password does not depend on that run; it comes from the direct comparison in IDA.

## Answer

Password:

```text
simba123
```
