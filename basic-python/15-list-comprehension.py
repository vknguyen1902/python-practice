fish = "halibut"

# 1. Loop through each letter in the string
# and push to an array
letters = []
for letter in fish:
    letters.append(letter)

print(f'1: {letters}')

# 2. List comprehensions provide concise syntax for creating lists
letters = [letter for letter in fish]

print(f'2: {letters}')

# 3. We can manipulate each element as we go
capital_letters = []
for letter in fish:
    capital_letters.append(letter.upper())

print(f'3: {capital_letters}')

# 4. List Comprehension for the above
capital_letters = [letter.upper() for letter in fish]

print(f'4: {capital_letters}')

# 5. We can also add conditional logic (if statements) to a list comprehension
july_temperatures = [87, 85, 92, 79, 106]
hot_days = []
for temperature in july_temperatures:
    if temperature > 90:
        hot_days.append(temperature)
print(f'5: {hot_days}')

# 6. List Comprehension with conditional
hot_days = [temperature for temperature 
            in july_temperatures 
            if temperature > 90]

print(f'6: {hot_days}')
