# copy_delete_files.py
import shutil
import os

source_file = "source_data.txt"
with open(source_file, "w") as f:
    f.write("Line 1: Hello!\n")
    f.write("Line 2: Python!\n")

print(f"Source file created.")

# Копируем
shutil.copy(source_file, "source_data_copy.txt")
print("File copied!")

# Бэкап
shutil.copy2(source_file, "source_data.bak")
print("Backup created!")

# Проверяем
for fname in [source_file, "source_data_copy.txt", "source_data.bak"]:
    print(f"  {'Done' if os.path.exists(fname) else 'Error'} {fname}")

# Удаляем
for fname in ["source_data_copy.txt", "source_data.bak", source_file]:
    if os.path.exists(fname):
        os.remove(fname)
        print(f"Deleted: {fname}")