# enumerate_zip_examples.py
from itertools import zip_longest

fruits = ["apple", "banana", "cherry"]
scores = [88, 72, 95]
names = ["Alice", "Bob", "Charlie"]
ages = [30, 25, 35]

# enumerate() — даёт индекс + значение
print("enumerate():")
for idx, fruit in enumerate(fruits, start=1):
    print(f"  {idx}. {fruit}")

# zip() — соединяет два списка попарно
print("\nzip():")
for name, age in zip(names, ages):
    print(f"  {name} is {age} years old")

# zip() → словарь
name_age = dict(zip(names, ages))
print("\nDict from zip:", name_age)

# enumerate + zip вместе
print("\nenumerate + zip:")
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"  {i}. {name} scored {score}")

# zip_longest
print("\nzip_longest:")
for pair in zip_longest([1, 2, 3], ["a", "b", "c", "d", "e"], fillvalue="—"):
    print(f"  {pair}")

# Проверка типов
print("\ntype checking:")
for val in [42, 3.14, "hi", True, [1, 2]]:
    print(f"  {val} → {type(val).__name__}")

# Конвертация типов
print("\ntype conversions:")
print("  int('5') =", int("5"))
print("  float('3.14') =", float("3.14"))
print("  str(100) =", str(100))
print("  list({1,2,3}) =", sorted(list({1, 2, 3})))