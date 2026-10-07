# #Worked 1
# def remaining(capacity, registered):
#   return capacity - registered

# value = remaining(20,2)
# print(value)
# print(remaining(registered=3, capacity=5))

# # Worked 2
# def greeting(name, prefix="Hello"):
#   return f"{prefix}, {name}"

# print(greeting('Amirul'))
# print(greeting('Amirul', prefix='Welcome'))

# # Worked 3
# def add_title(title, titles=None):
#   if titles is None:
#     titles = []
#   return [*titles, title] # * will unpack the array/list

# print(add_title('Python'))
# print(add_title('SQL'))
# print(add_title('React', ['Python', 'JS']))

# # Example 1
# def remaining_seats(capacity, registered):
#   return capacity - registered

# print(remaining_seats(20,8))

# # Example 2
# def normalize_email(email=None):
#   if email is None:
#     return 'Empty'
#   else:
#     return email.lower()

# print(normalize_email('ADA@EMAIL.COM'))
# print(normalize_email())
  
# # Example 3
# def with_registration(ids, participant_id):
#   newList = [ids, participant_id]
#   return list(dict.fromkeys(newList))

# print(with_registration('p1', 'p2'))
# print(with_registration('p1', 'p1'))