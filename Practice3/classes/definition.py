#1
class MyClass:
  x = 5 #<class '__main__.MyClass'>

#2
p1 = MyClass()
print(p1.x) #5

#3
del p1

#4
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

