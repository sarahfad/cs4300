import math

def define_number(num):
    """
    Return 'positive', 'negative', or 'zero' for an integer.
    """
    if type(num) is bool or not isinstance(num, int):
        raise TypeError("num must be an int") #explicitly state that bools are not allowed, and only ints are
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"


def is_prime(num):
    """
    Return True if num is prime (num >= 2), else False.
    """
    if type(num) is bool or not isinstance(num, int):
        raise TypeError("num must be an int") #explicitly state that bools are not allowed, and only ints are
    if num <= 1:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0:
        return False
  
    limit = int(math.isqrt(num))
    for i in range(3, limit + 1, 2):
        if num % i == 0:
            return False
    return True


def first_10_primes():
    """
    Return the first 10 prime numbers as a list.
    """
    result = []
    candidate = 2
    while len(result) < 10:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1
    return result


def print_first_10_primes():
    """
    Print the first 10 primes.
    """
    for p in first_10_primes():
        print(p)


def sum_1_to_100():
    """
    Compute the sum 1 through 100 using a while loop  
    """
    total = 0
    num = 1
    while num <= 100:
        total += num
        num += 1
    return total


if __name__ == "__main__":
    print("define_number:", define_number(5), define_number(-1), define_number(0))
    print("First 10 primes:")
    print_first_10_primes()
    print("Sum 1 - 100:", sum_1_to_100())
