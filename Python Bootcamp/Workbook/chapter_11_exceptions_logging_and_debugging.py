# # Worked 1
# text = '20'
# try:
#   capacity = int(text)
# except ValueError: 
#   print('Enter a whole number')
# else:
#   print(capacity)

# # Worked 2
# def valid_capacity(value):
#   if type(value) is not int or not 1 <= value <= 500:
#     raise ValueError('Capacity must be an integer from 1 to 500')
#   return value
# print(valid_capacity(20))

# # Worked 3
# import logging

# logger = logging.getLogger('workshop_hub')
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# workshop_id = 'w1'
# logger.info('Workshop update rejected: id=%s reason=capacity', workshop_id)

# # Exercise 1
# def parse_capacity(text):
#   try:
#     capacity = int(text)
#   except ValueError:
#     return 'Rejected: Not a valid value'
#   if 0 < capacity < 501:
#     return 'Accepted'
#   return 'Rejected: Not inside range'

# print(parse_capacity('500'))
# print(parse_capacity('501'))
# print(parse_capacity('abc'))

# # Exercise 2
# def parse_count(text):
#   try:
#     return int(text)
#   except ValueError as error:
#     raise ValueError('Count must be a whole number') from error


# print(parse_count('3'))

# try:
#   parse_count('abc')
# except ValueError as error:
#   print(f'Invalid count: {error}')

# Exercise 3