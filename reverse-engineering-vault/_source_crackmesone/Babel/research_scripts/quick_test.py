import subprocess
binary = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"

tests = [
    ("test", "44AA-322B-6075-B7AD-F397-BAD5-BAD6-BAD7"),
    ("test", "44AA-322B-6075-B7AD-F397-0000-0000-0000"),
]

for username, serial in tests:
    inp = f"{username}\n{serial}\n"
    r = subprocess.run([binary], input=inp, capture_output=True, text=True, timeout=10)
    result = "Access Granted" if "Access Granted" in r.stdout else "Invalid License" 
    print(f"{username} / {serial} => {result}")
