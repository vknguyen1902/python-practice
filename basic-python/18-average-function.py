def average(numbers):
    length = len(numbers)
    total = 0.0
    for number in numbers:
        total += number
    return total / length

print(average([1,5,9]))
print(average(range(11)))
    