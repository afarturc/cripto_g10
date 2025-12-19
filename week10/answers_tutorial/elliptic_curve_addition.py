def elliptic_curve_addition(elliptic_curve, p, q) -> tuple[object, object]:
    #NOTE Let's define elliptic_curve variables as a tuple (a, b) where a, b are the values from
    # y^2 = x^3 + ax + b.
    
    #NOTE: In our implementation, let's represent O = (None, None)
    # where O = (x, y) + (x, -y)
    
    O = (None, None)
    
    if p == O:
        return q
    
    if q == O:
        return p
    
    if p[0] == q[0] and p[1] == -q[1]:
        return O
    
    
    lambda_var = calc_lambda(elliptic_curve, p, q)
    
    x3 = lambda_var ** 2 - p[0] - q[0]
    y3 = lambda_var * (p[0] - x3) - p[1]
    
    return (x3, y3)
    

def calc_lambda(elliptic_curve: tuple[float, float], 
                p: tuple[float, float], 
                q: tuple[float, float]) -> float:
    if p != q:
        return (q[1] - p[1]) / (q[0] - p[0])
    else: # p == q
        return (3*(p[0]**2) + elliptic_curve[0]) / (2 * p[1])
    
    