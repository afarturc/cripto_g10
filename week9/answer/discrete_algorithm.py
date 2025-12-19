import math

def discrete_algorihtm(b: int, n: int, base: int = 2) -> list[int]:
    "base^x = b (n) where = is congruency modulo n"
    
    m:int = math.ceil(math.sqrt(n-1))
    
    
    baby_steps = {}  # List to store precomputed powers of 2
    for j in range(m):
        baby_steps[pow(base, j, n)] = j
    
    alpha_m = pow(base, m, n)
        
    a_to_minus_m:int = pow(alpha_m, -1, n)
    
    y = b
    
    results = []
    for i in range(m):
        if y in baby_steps:
            j = baby_steps[y]
            x = i * m + j
            if(x < n):
                results.append(x)
        y = (y * a_to_minus_m) % n
    
    return results



