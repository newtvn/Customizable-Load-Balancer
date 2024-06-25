import random
import string

def get_random_number(length: int) -> int:
    output = ''.join(random.choices(string.digits, k=length))
    
    return int(output)