candyList = ["Snickers", "Kit Kat", "Sour Patch Kids", "Juicy Fruit", "Swedish Fish",
             "Skittles", "Hershey Bar", "Skittles", "Starbursts", "M&Ms"]

allowance = 5
i = 0

candyCart = []

for candy in candyList:
    print('[' + str(candyList.index(candy)) + "] " + candy)

while i < allowance:
    inCart = int(input('What is your candy index? '))
    candyCart.append(candyList[inCart])
    i = i + 1

print(candyCart)