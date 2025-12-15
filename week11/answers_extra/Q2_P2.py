import random

def recover_polynomial(points):
    
    def polynomial(x):
        
        result = 0
        
        for point in points:
            xi, yi = point
            
            
            Li_num = 1
            Li_den = 1
            for j in range(len(points)):
                if points[j] == point:
                    continue
                
                xj, _ = points[j]
                
                Li_num *= (x - xj)   # (x - xi)
                Li_den *= (xi - xj)
                
                
            Li = Li_num / Li_den    
            result += yi * Li
        
        # Use of round function because of strange behaviour caused with how numbers are represented in binary
        # In some test done, the result given was 1001.0000000000073. There are some tests as well for values 
        # lower than the one that should be
        
        return round(result)
    
    return polynomial
        
        
## let's create the polynomial f(x) = 1001 + 34x + 21x^2

def generates_polynomial(secret, degree, max_coefficient = 100):
    
    coefficients = []
    coefficients.append(secret)
    
    for i in range(1, degree):
        
        lower_bound = 1 if i == degree - 1 else 0
        coefficients.append(random.randint(lower_bound, max_coefficient))
    
    
    return lambda x: sum(coef * (x ** power) for power, coef in enumerate(coefficients))


def generates_shares(polynomial, shares, max_x = 100):
    points = []
    x_values = []
    for _ in range(shares):
        x =  random.randint(1, max_x)
        if x not in x_values:
            x_values.append(x)
            points.append((x, polynomial(x)))
    
    return points
        
