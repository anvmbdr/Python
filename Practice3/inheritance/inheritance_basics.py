class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

#2
class Student(Person):
  pass

#3
x = Student("Mike", "Olsen")
x.printname()

#4
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#5
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

