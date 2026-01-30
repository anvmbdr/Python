#ARITHMETIC
x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y) #float
print(x % y)
print(x ** y)
print(x // y) #returns int, rounds down to the nearest int

#ASSIGNMENT #waltus operator
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements") #The count variable is assigned in the if statement, and given the value 5:

#COMPARISON
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

#CHAINING COMPARISON
x = 5

print(1 < x < 10)

print(1 < x and x < 10)

#LOGICAL
x = 5

print(x > 0 and x < 10)

#LOGICAL2
x = 5

print(x > 0 and x < 10)

#LOGICAL3
x = 5

print(not(x > 3 and x < 10))

#IDENTITY
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)

#IDENTITY2
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)

#iDENTITY3
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)#TRUE. Checks if the values of both variables are equal
print(x is y)#FALSE. Checks if both variables point to the same object in memory

#MEMBERSHIP
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)

#MEMBERSHIP2
fruits = ["apple", "banana", "cherry"]

print("pineapple" not in fruits)

#MEMBERSHIP3
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)

#BITWISE
print(6 & 3)#2. compares each bit and set it to 1 if both are 1, otherwise it is set to 0:

#BITWISE2
print(6 | 3)#7. compares each bit and set it to 1 if one or both is 1, otherwise it is set to 0:

#BITWISE3
print(6 ^ 3)#5.  compares each bit and set it to 1 if only one is 1, otherwise (if both are 1 or both are 0) it is set to 0:

#PRECEDENCE
print((6 + 3) - (6 + 3))
print(100 + 5 * 3)
print(5 + 4 - 7 + 3)






