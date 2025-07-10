import subprocess
import sys

# Run the test and capture output
proc = subprocess.Popen(
    [sys.executable, "-m", "maniml", "test_duplicate_debug.py", "TestDuplicateDebug"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Print output line by line, highlighting important parts
for line in proc.stdout:
    line = line.rstrip()
    if "[DEBUG" in line or "[TEST" in line or "CHECKPOINT" in line:
        print(line)
    elif "Circle" in line or "Square" in line:
        print(f">>> {line}")
    elif "checkpoint" in line.lower():
        print(f"==> {line}")

proc.wait()