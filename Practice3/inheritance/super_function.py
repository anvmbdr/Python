# Example 1
class A:
    def hello(self):
        print("Hello from A")
class B(A):
    def hello(self):
        super().hello()
        print("Hello from B")
b = B()
b.hello()
# Hello from A
# Hello from B

# Example 2
class Parent:
    def greet(self):
        print("Parent greeting")
class Child(Parent):
    def greet(self):
        super().greet()
        print("Child greeting")
c = Child()
c.greet()
# Parent greeting
# Child greeting

# Example 3
class Vehicle:
    def wheels(self):
        print("Vehicle has wheels")
class Car(Vehicle):
    def wheels(self):
        super().wheels()
        print("Car has 4 wheels")
car = Car()
car.wheels()
# Vehicle has wheels
# Car has 4 wheels

# Example 4
class Animal:
    def eat(self):
        print("Animal eats")
class Cat(Animal):
    def eat(self):
        super().eat()
        print("Cat eats fish")
cat = Cat()
cat.eat()
# Animal eats
# Cat eats fish
