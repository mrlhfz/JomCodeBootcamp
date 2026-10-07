# # Worked 1
# def remaining(capacity: int, registered: int) -> int:
#   return capacity - registered

# print(remaining(20,8))
# print(remaining.__annotations__)

# # Worked 2
# from dataclasses import dataclass

# @dataclass
# class Workshop:
#   title: str
#   capacity: int

# workshop = Workshop('Python', 10)
# print(workshop.title, workshop.capacity)

# Worked 3
class Calculator: 
  def __init__(self, operation):
    self.operation = operation

  def apply(self, value):
    return self.operation(value)

def double(value):
  return value * 2

print(Calculator(double).apply(3))