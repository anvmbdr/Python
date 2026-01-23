#1
x = 5
y = "John"
print(x)
print(y)

#2
x = 4      
x = "Sally" 
print(x)

#3
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

#4
x = 5
y = "John"
print(type(x))
print(type(y))

#5
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#6
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#7 ERROR
x = 5
y = "John"
print(x + y)

#8 OK
x = 5
y = "John"
print(x, y)

#9
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)