import random
import time
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_cache(func):
    def wrapper(*args, **kwargs):
        number = args[0]
        cache_val = r.get(str(number))
        if cache_val is None:
            val = func(*args, **kwargs)
            r.set(str(number), str(val), ex=60)
        else:
            val = int(cache_val)
        return val
    return wrapper


def count_factorial_cache(n):
    if n == 0:
        return 1
    cache_val = r.get(str(n))
    if cache_val is None:
        num = n * count_factorial(n-1)
        r.set(str(n), str(num), ex=60)
    else:
        num = int(cache_val)
    return num


@check_cache
def count_factorial_deco(n):
    if n == 0:
        return 1
    return n * count_factorial(n-1)


def count_factorial(n):
    if n == 0:
        return 1
    return n * count_factorial(n-1)


# Cache on
t1 = time.time()
for i in range(1, 1000):
    number = random.randint(1, 500)
    a = count_factorial_deco(number)
t2 = time.time()

print(t2 - t1)

r.close()


# Without cache
t1 = time.time()
for i in range(1, 1000):
    number = random.randint(1, 500)
    a = count_factorial(number)
    # r.set(str(number)+"_nocache", str(a), ex=60)
    r.get(str(number)+"_nocache")
t2 = time.time()

print(t2 - t1)
