from random import randint


def pay_kuai3(content_list: str, amount: int):
    # 抽成
    draw = 0.001
    money = 0
    # 掷骰子3d6
    a = randint(1, 6)
    b = randint(1, 6)
    c = randint(1, 6)
    total = a + b + c
    big_or_small = "大" if total >= 11 else "小"
    odd_or_even = "单" if total % 2 else "双"
    # 结算
    for content in content_list:
        print(content)
        if content in [big_or_small, odd_or_even]:
            print("1.yml")
            money += amount * (2 - draw)

    return {
        'money': round(money, 2),
        'a': a,
        'b': b,
        'c': c,
        'total': total,
        'big_or_small': big_or_small,
        'odd_or_even': odd_or_even
    }


def insertionBlanks(matched):
    return " ".join(matched.group())
