import subprocess
import sys

binary = r"c:\Users\hatem\Desktop\Challenges\Challenge03\69ca6a30f2d49d8512f64bcc\babel_vm.exe"

username = "test"
serial = "247E-322B-4819-E41F-F52A-718B-670A-2D42"

inp = f"{username}\n{serial}\n"

result = subprocess.run(
    [binary],
    input=inp,
    capture_output=True,
    text=True,
    timeout=10
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
