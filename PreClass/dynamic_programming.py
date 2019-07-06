from collections import defaultdict
from functools import lru_cache

length_prices_v = {
    1: 1,
    2: 5,
    3: 8,
    4: 9,
    5: 10,
    6: 17,
    7: 17,
    8: 20,
    9: 24,
    10: 30
}
'''
length_prices_v = {
    1: 1,
    2: 5,
    3: 2,
    4: 9,
    5: 10,
    6: 17,
    7: 17,
    8: 20,
    9: 2,
    10: 3
}'''

length_prices = defaultdict(int)

for k, v in length_prices_v.items():
    length_prices[k] = v

solution = {}
#index = 0


@lru_cache(maxsize=2*10)
def revenue(length, index):
    index += 1
    candidates_price = [((0, length), length_prices[length])] + \
                       [((cut, length-cut), revenue(cut, index) + revenue(length - cut, index)) for cut in range(1, length)]
    print(candidates_price, end='        ')
    print(index)
    split, value = max(candidates_price, key=lambda x: x[1])
    solution[length] = split
    return value


print(revenue(20, 0))

print(solution)