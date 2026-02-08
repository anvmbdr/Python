#1
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#2
def get_greeting():
  return "Hello from a function"

print(get_greeting())

#3
def my_function():
  pass

#4
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

#5
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

#6
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y) #returns tuple

#7
def my_function(name, /):
  print("Hello", name)

my_function("Emil") #You can specify that a function can have ONLY positional arguments.

#8
def my_function(name):
  print("Hello", name)

my_function(name = "Emil")

#9Error
def my_function(name, /):
  print("Hello", name)

my_function(name = "Emil")

#10
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil") #keyword-only arguments

#11Error
def my_function(*, name):
  print("Hello", name)

my_function("Emil")

