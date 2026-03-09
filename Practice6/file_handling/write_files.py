# write_files.py

filename = "sample_data.txt"

with open(filename, "w") as f:
    f.write("Name, Age, City\n")
    f.write("Alice, 30, New York\n")
    f.write("Bob, 25, Los Angeles\n")
    f.write("Charlie, 35, Chicago\n")

print(f"✅ File '{filename}' created!")

with open(filename, "a") as f:
    f.write("Diana, 28, Houston\n")
    f.write("Eve, 22, Phoenix\n")

print(f"✅ New lines appended!")

print("\n📄 File contents:")
with open(filename, "r") as f:
    for line_num, line in enumerate(f, start=1):
        print(f"  Line {line_num}: {line}", end="")