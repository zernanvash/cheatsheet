# Simple login crackme Writeup

Challenge_URL: https://crackmes.one/crackme/69e13f938afd9d6c48b488fd

How I Achieved This
Code Reconstruction: I analyzed the main function using IDA Pro. I noticed that the pseudocode was misleading and missed crucial steps. By switching to Assembly Graph View, I found the real logic inside the loc_7FF6F774137D block, which revealed that the result was multiplied by 0x539 (1337) and then XORed with 0x5A5A (23130) before comparison.
Dynamic Verification: I used the IDA Local Debugger to confirm my theory. I set a breakpoint right before the password check and inspected the RDX register. By entering test usernames like A and DevVolodya, I captured the exact hex values the program was calculating.
Algorithm Alignment: I matched the debugger's output with my Python implementation. I used ctypes to ensure the script handled 32-bit signed integer overflows exactly like a C++ application on Windows.
Full Automation: I combined the verified algorithm with a Python subprocess handler. This allowed me to automate the entire process: calculating the key, launching the executable, and injecting the credentials into the process memory.
Final Keygen Script
python
import subprocess
import time
import ctypes

def generate_key(username):
    v4 = 0
    for i, char in enumerate(username):
        eax = (ord(char) * (i + 1) + v4) & 0xFFFFFFFF
        v4 = (eax ^ (eax << 3)) & 0xFFFFFFFF
    
    res = (v4 * 0x539) & 0xFFFFFFFF
    res = (res ^ 0x5A5A) & 0xFFFFFFFF
    
    return str(ctypes.c_int32(res).value)

def main():
    username = input("Enter username: ")
    password = generate_key(username)
    
    exe_path = r"C:\Users\DevVolodya\Downloads\crackme\noncrack\crackmepls.exe"
    
    try:
        proc = subprocess.Popen(
            exe_path, 
            stdin=subprocess.PIPE, 
            text=True
        )
        
        proc.stdin.write(username + "\n")
        proc.stdin.flush()
        time.sleep(0.3)
        proc.stdin.write(password + "\n")
        proc.stdin.flush()
        proc.wait()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()