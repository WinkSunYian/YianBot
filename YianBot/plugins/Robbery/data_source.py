from random import randint


def play(my, target):
    num = 20
    a = my if num > my else num
    b = target if num > target else num + int(target ** (1 / 3))
    return randint(-a, b)


m = play(50000, 30)
print(m)
