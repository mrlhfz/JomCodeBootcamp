# workshop = {
#   'id': 'w1',
#   'title': 'Python',
#   'capacity': 20
# }
# print(workshop['title'])
# print(workshop.get('venue', 'TBC'))
# print('title' in workshop)
# workshop.setdefault('venue', 'TBC')
# print(workshop)



# participant_ids = ['u2', 'u1', 'u4']
# unique_ids = set(participant_ids)
# print(sorted(unique_ids))
# print('u1' in unique_ids)
# print(unique_ids & {'u1', 'u3'})
# print(sorted(participant_ids))



# workshops = [
#   {
#     'id': 'w1',
#     'capacity': 0
#   },
#   {
#     'id': 'w2',
#     'capacity': 50
#   },
#   {
#     'id': 'w3',
#     'capacity': 1
#   }
# ]
# open_ids = [workshop['id'] for workshop in workshops if workshop['capacity'] > 0]
# print(open_ids)



# normal_list = ['p3', 'p2', 'p1', 'p3']
# #list way
# normal_list = sorted(list(dict.fromkeys(normal_list)))
# print(normal_list)
# #set way
# sorted_normal_set = sorted(set(normal_list)) #sorted() always returns as list
# unsorted_normal_set = set(normal_list)
# print(sorted_normal_set)
# print(unsorted_normal_set)



workshops = [
  {
    'id': 'w1',
    'capacity': 50
  },
  {
    'id': 'w2',
    'capacity': 100
  },
]
total = 0
for workshop in workshops:
  total += workshop['capacity']
print(total) #1
total = sum(workshop['capacity'] for workshop in workshops)
print(total) #2
check0 = sum(workshop['capacity'] == 0 for workshop in workshops)
print(f'Empty => {check0}')
