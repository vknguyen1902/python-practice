play = 'y'
index = 0

while play == 'y':   
    ask = int(input("How many numbers? "))

    while index <= ask:
        print(index)
        index = index + 1
    play = input('Type y to continue or n to stop: ')
