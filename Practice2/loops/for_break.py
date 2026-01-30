#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#3
for i in range(1, 6):
    print(i)
    if i == 3:
        break  # 1
                 # 2
                 # 3

#4
for ch in "hello":
    print(ch)
    if ch == "l":
        break  # h
                 # e
                 # l

#5
colors = ["red", "green", "blue", "yellow"]
for color in colors:
    if color == "blue":
        break
    print(color)  # red
                  # green
