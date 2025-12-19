import sage.all as sage
import random

def find_k_and_d(n: int) -> tuple[int, int]:
    "Finds k and d such that n - 1 = 2^k * d with d odd."
    d =  n - 1
    k = 0
    
    while d % 2 == 0:
        d = d // 2
        k += 1

    return k, d
    
    
def witness(n: int, a: int) -> bool:
    
    """
    Returns True if a^d !== 1 (mod n) and a^(2^(i)*d) !== 1 (mod n) (=== representing congruency) 
    and False otherwise. The values of i are from {1, 2, ... , k}.
    
    The value of k and d are calculated such as n - 1 = 2^k * d.
    """
    
    gcd = sage.gcd(n, a)
    assert gcd == 1, f"n = {n} and a = {a} must be coprime, but sage.gdc(n, a) = {gcd}"
    
    k, d = find_k_and_d(n)
    
    x = sage.power_mod(a, d, n)
    if x == 1 or x == n - 1:
        return False
    
    minus_one = sage.mod(-1, n)
    
    for i in range(1, k + 1):
        x = sage.power_mod(x, 2, n)
        if x == minus_one:
            return False
        
    return True
        


def isPrime(n: int, m: int) -> tuple[bool, float]:
    """
    It checks if a big integer is a prime, if it is True, then this is with a probability of 1 - 2^m 
    """
    
    for _ in range(m):
        a = random.randint(2, n - 2)
        if witness(n, a):
            
            return (False, 1.0) # if it does not succedd, we already know that is NOT a prime number
        
    return (True, 1 - sage.power(2, -m))




