names = []
for _ in range(5):
    name = input("Please enter a name: ")
    names.append(name)

#Use list comprehension to create list of lowercased names
lowercased = [name.lower() for name in names]

#Use list comprehension to create list of titlecased names
titlecased = [name.title() for name in lowercased]

invitations = [f"Dear {name}, please come to our wedding this Saturday!" 
                 for name in titlecased]

for invitation in invitations: 
    print(invitation)

