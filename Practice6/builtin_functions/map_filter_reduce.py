# map_filter_reduce.py
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words = ["hello", "world", "python", "is", "awesome"]

# map() — применяет функцию к каждому элементу
squares = list(map(lambda x: x ** 2, numbers))
uppercased = list(map(str.upper, words))
print("map() squares:", squares)
print("map() upper:", uppercased)

# filter() — оставляет только подходящие элементы
evens = list(filter(lambda x: x % 2 == 0, numbers))
long_words = list(filter(lambda w: len(w) > 4, words))
print("\nfilter() evens:", evens)
print("filter() long words:", long_words)

# reduce() — сворачивает список в одно значение
total = reduce(lambda a, b: a + b, numbers)
product = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])
print("\nreduce() sum:", total)
print("reduce() product:", product)