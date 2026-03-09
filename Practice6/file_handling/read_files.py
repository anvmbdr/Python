# read_files.py

filename = "sample_data.txt"

with open(filename, "w") as f:
    f.write("Name, Age, City\n")
    f.write("Alice, 30, New York\n")
    f.write("Bob, 25, Los Angeles\n")

# Метод 1
print("Method 1 - read():")
with open(filename, "r") as f:
    print(f.read())

# Метод 2
print("Method 2 - readlines():")
with open(filename, "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        print(f"  [{i}] {line.strip()}")

# Метод 3
print("\nMethod 3 - direct loop:")
with open(filename, "r") as f:
    for line in f:
        print(f"  {line.strip()}")