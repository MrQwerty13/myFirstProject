import random
import os

max = os.getenv("MAX_VALUE")
min = os.getenv("MIN_VALUE")


def give_a_num(minim, maxim):
    try:
        return random.randint(int(minim), int(maxim))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(min, max)
    print(give_a_num(min, max))
