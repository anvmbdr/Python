#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#2
for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)  # 1
              # 3
              # 5

#3
for ch in "hello":
    if ch == "l":
        continue
    print(ch)  # h
              # e
              # o

#4
items = [10, "apple", 3.14, "banana"]
for item in items:
    if isinstance(item, str):
        continue
    print(item)  # 10
                  # 3.14

#5
words = ["cat", "dog", "bird", "fish"]
for w in words:
    if "i" in w:
        continue
    print(w)  # cat
              # dog
