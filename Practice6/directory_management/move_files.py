# move_files.py
import os
import shutil

# Создаём папки и файлы
os.makedirs("workspace/inbox", exist_ok=True)
os.makedirs("workspace/archive", exist_ok=True)

for name in ["report.txt", "notes.txt", "data.csv"]:
    with open(f"workspace/inbox/{name}", "w") as f:
        f.write(f"Content of {name}\n")

print(" Inbox:", os.listdir("workspace/inbox"))

# Перемещаем один файл
shutil.move("workspace/inbox/notes.txt", "workspace/archive/notes.txt")
print(" Moved notes.txt → archive/")

# Копируем папку целиком
shutil.copytree("workspace/archive", "workspace/archive_backup")
print(" Copied archive/ → archive_backup/")

# Итог
print("\n Final contents:")
for folder in ["inbox", "archive", "archive_backup"]:
    path = f"workspace/{folder}"
    print(f"  {folder}: {os.listdir(path)}")

shutil.rmtree("workspace")
print("\n Cleanup done.")