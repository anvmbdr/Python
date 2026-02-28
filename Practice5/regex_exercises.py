import re

#1 'a' followed by zero or more 'b's
pattern1 = re.compile(r"ab*")
print("#1:", pattern1.findall("ac abc abbc"))
#1: ['a', 'ab', 'abb']

#2 'a' followed by two to three 'b's
pattern2 = re.compile(r"ab{2,3}")
print("#2:", pattern2.findall("ab abb abbb abbbb"))
#2: ['abb', 'abbb', 'abbb']

#3 sequences of lowercase letters joined with underscore
pattern3 = re.compile(r"[a-z]+_[a-z]+")
print("#3:", pattern3.findall("hello_world foo_bar ABC test"))
#3: ['hello_world', 'foo_bar']

#4 one uppercase letter followed by lowercase letters
pattern4 = re.compile(r"[A-Z][a-z]+")
print("#4:", pattern4.findall("Hello World foo BAR Python"))
#4: ['Hello', 'World', 'Python']

#5 'a' followed by anything, ending in 'b'
pattern5 = re.compile(r"a.*b")
print("#5:", pattern5.findall("aXYZb ab acb"))
#5: ['aXYZb ab acb']

#6 replace space, comma, dot with colon
s6 = "one two,three.four"
result6 = re.sub(r"[ ,.]", ":", s6)
print("#6:", result6)
#6: one:two:three:four

#7 snake_case to camelCase
s7 = "hello_world_foo"
result7 = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s7)
print("#7:", result7)
#7: helloWorldFoo

#8 split string at uppercase letters
s8 = "HelloWorldFoo"
result8 = re.split(r"(?=[A-Z])", s8)
print("#8:", result8)
#8: ['', 'Hello', 'World', 'Foo']

#9 insert spaces between words starting with capital letters
s9 = "HelloWorldFoo"
result9 = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s9)
print("#9:", result9)
#9: Hello World Foo

#10 camelCase to snake_case
s10 = "helloWorldFoo"
result10 = re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), s10)
print("#10:", result10)
#10: hello_world_foo