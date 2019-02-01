import random

result = ['r', 'p', 's']
hand = input("Type r, p, s for rock, paper, scissor: ")
comp = random.choice(result)

print("The computer gets " + comp)

if hand == comp:
    print("Tied")
elif (hand=='r' and comp=='s') or (hand=='s' and comp=='p') or (hand=='p' and comp=='r'):
    print('You win')  
else:
    print('You lose')
