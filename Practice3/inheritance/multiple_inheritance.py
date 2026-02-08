# Example 1
class A:
    def greet(self):
        print("Hello from A")
class B:
    def greet(self):
        print("Hello from B")
class C(A, B):
    pass
c = C()
c.greet()  # Hello from A

# Example 2
class X:
    def feature(self):
        print("Feature X")
class Y:
    def feature(self):
        print("Feature Y")
class Z(X, Y):
    pass
z = Z()
z.feature()  # Feature X

# Example 3
class Parent1:
    def method(self):
        print("Parent1 method")
class Parent2:
    def method(self):
        print("Parent2 method")
class Child(Parent1, Parent2):
    pass
ch = Child()
ch.method()  # Parent1 method

# Example 4
class A:
    def show(self):
        print("A show")
class B:
    def show(self):
        print("B show")
class C(B, A):
    pass
c = C()
c.show()  # B show
