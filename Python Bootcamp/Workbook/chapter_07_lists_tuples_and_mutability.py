# titles = ["Python"]
# titles.append("Web")
# titles.extend(["SQL", "React"])
# titles.pop()
# removed = titles.pop()

# print(f"{titles}")
# print(f"{removed}")



# letters = ["a", "b"]
# letters.append("c")
# letters.extend("laptop")

# print(f"{letters}")



# titles = ["Python", "SQL"]
# alsoTitlesButDiffABit = titles.copy()

# alsoTitlesButDiffABit.append("React")

# print(f"{titles}")
# print(f"{alsoTitlesButDiffABit}")



# dimensions = (1280, 720)
# width, height = dimensions 

# print(width, height)
# print(dimensions[:1])


import copy

ori = [[1, 2], [3, 4]]
spicy = copy.deepcopy(ori)

spicy[0].append("99")
print(f"{ori}")
print(f"{spicy}")