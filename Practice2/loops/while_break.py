#1
i = 0
while i < 5:
    i += 1
    if i == 2:
        continue
    print(i)  # 1
              # 3
              # 4
              # 5

#2
i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print(i)  # 1
              # 3
              # 5

#3
i = 1
while i <= 7:
    if i == 4 or i == 6:
        i += 1
        continue
    print(i)  # 1
              # 2
              # 3
              # 5
              # 7
    i += 1

#4
i = 0
while i < 8:
    i += 1
    if i > 5:
        continue
    print(i)  # 1
              # 2
              # 3
              # 4
              # 5

#5
i = 0
while i < 10:
    i += 1
    if i % 3 == 0:
        continue
    print(i)  # 1
              # 2
              # 4
              # 5
              # 7
              # 8
              # 10
