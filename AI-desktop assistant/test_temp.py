import random
import concurrent.futures

def generate_random_number(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(random.randint(10, 15))])


length = random.randint(10, 15)
print(generate_random_number(length))
