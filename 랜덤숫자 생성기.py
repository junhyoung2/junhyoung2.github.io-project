import random

def generate_random_number(min_val, max_val):
    if min_val > max_val:
        raise ValueError("Min should be less than max")
    return random.randint(min_val, max_val)

if __name__ == "__main__":
    print("Random Number:", generate_random_number(1, 180))
