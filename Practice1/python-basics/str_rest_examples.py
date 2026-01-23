age = 36
txt = f"My name is John, I am {age}"
print(txt)

a = "Hello"
b = "World"
c = a + " " + b
print(c) #otherwise jabysyp qalad

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt) #The price is 59.00 dollars

txt = f"The price is {20 * 59} dollars"
print(txt) #The price is 1180 dollars

#ESCAPE CHARACTERS

#1 ERROR
txt = "We are the so-called "Vikings" from the north."

#2 OK
txt = "We are the so-called \"Vikings\" from the north."

#3
txt = 'It\'s alright.'
print(txt) 

#4
txt = "This will insert one \\ (backslash)."
print(txt) 

#5
txt = "Hello\nWorld!"
print(txt) #new line

#6
txt = "Hello\rWorld!"
print(txt) #World!

#7
txt = "Hello\tWorld!"
print(txt)  #Hello   World!

#This example erases one character (backspace):
txt = "Hello \bWorld!"
print(txt) 

