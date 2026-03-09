# create_list_dirs.py
import os
import glob
import shutil

# Создаём вложенные папки
os.makedirs("project_root/src/utils", exist_ok=True)
os.makedirs("project_root/data/raw", exist_ok=True)
os.makedirs("project_root/logs", exist_ok=True)
print(" Nested directories created!")

# Создаём файлы внутри
open("project_root/src/utils/helpers.py", "w").close()
open("project_root/data/raw/data.csv", "w").close()
open("project_root/logs/app.log", "w").close()

# Показываем дерево папок
print("\n Directory tree:")
for root, dirs, files in os.walk("project_root"):
    level = root.count(os.sep)
    indent = "    " * level
    print(f"{indent}📁 {os.path.basename(root)}/")
    for file in files:
        print(f"{indent}     {file}")

# Ищем по расширению
print("\n Python files:")
for f in glob.glob("project_root/**/*.py", recursive=True):
    print(f"  → {f}")

print("\n Log files:")
for f in glob.glob("project_root/**/*.log", recursive=True):
    print(f"  → {f}")

shutil.rmtree("project_root")
print("\n Cleanup done.")