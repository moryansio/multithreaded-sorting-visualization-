import random

def generate_strict_random(n: int, a: int = 0, b: int = 100_000) -> list[int]:
    
    return [random.randint(a, b) for _ in range(n)]

def generate_reverse_sorted_random(n: int, a: int = 0, b: int = 100_000) -> list[int]:
    
    arr = [random.randint(a, b) for _ in range(n)]
    arr.sort(reverse=True)
    return arr