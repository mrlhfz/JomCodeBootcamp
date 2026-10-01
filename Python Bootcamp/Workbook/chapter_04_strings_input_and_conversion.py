# title = "Pythin"
# print(title[0], title[4])
# print(title[:3])
# print(title[3:])
# print(title[20:])

# name = "  Ada  Lovelace  "
# email = "  ADA@EXAMPLE.COM  "
# print(name.strip())
# print(email.strip().lower())

capacity_text = input("Capacity: ")
registered_text = input("Registered: ")
capacity = int(capacity_text)
registered = int(registered_text)
print(f"Remaining: {capacity - registered}")