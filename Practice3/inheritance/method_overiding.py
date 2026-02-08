# Example 1
class A:
    def greet(self):
        print("Hello from A")
class B(A):
    def greet(self):
        print("Hello from B")
b = B()
b.greet()  # Hello from B

# Example 2
class Shape:
    def area(self):
        print("Area unknown")
class Circle(Shape):
    def area(self):
        print("Area = πr²")
c = Circle()
c.area()  # Area = πr²

# Example 3
class Vehicle:
    def wheels(self):
        print("Unknown wheels")
class Bike(Vehicle):
    def wheels(self):
        print("2 wheels")
bike = Bike()
bike.wheels()  # 2 wheels

# Example 4
class Animal:
    def sound(self):
        print("Some sound")
class Dog(Animal):
    def sound(self):
        print("Bark")
d = Dog()
d.sound()  # Bark
