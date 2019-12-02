#!/usr/bin/env python3

class Fibonacci(object):

    def __init__(self, end=20):
        self.a = 0
        self.b = 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.b >= self.end:
            raise StopIteration
        return self.b

for i in Fibonacci(40):
    print(i)
