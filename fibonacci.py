import redis


r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def check_cache(prefix: str, ttl: int=60):
    def deco(func):
        def wrapper(n: int):
            key = f"{prefix}:{n}"
            cache_val = r.get(key)
            if cache_val is None:
                val = func(n)
                r.set(key, str(val), ex=ttl)
                return val
            return int(cache_val)
        return wrapper
    return deco


@check_cache(prefix='fib', ttl=60)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))

r.close()