from constants import constants
from sage.all import Integer, GF, EllipticCurve, inverse_mod
import secrets
import hashlib
# Let's import the constants given for P-192, made in a tuple just
# so there is no risk of changing a constant

Fp = GF(constants.p)
E = EllipticCurve(Fp, [constants.a, constants.b])
G = E(constants.Gx, constants.Gy)

# Let's do some basic validations first

assert G in E, "Generator G is NOT on the curve"
assert (constants.n * G).is_zero(), "n*G is not the point at infinity (generator order mismatch)"


def generate_keys():
    """It returns a ECDSA valid key pair. Important to import 
    the constants from constants.py

    Returns:
        tuple: (d, Q) being d the private key and Q the public key
    """


    print("P-192 curve instantiated.")
    print(f"Field prime p bit-length: {constants.p.nbits()}")
    print(f"Generator G: {G}")
    print(f"n * G is infinity? -> {(constants.n * G).is_zero()}")


    # Let's produce a cryptographically secure random number generator
    # NOT the random library

    # Generate private key d
    #NOTE: 1 <= d <= n - 1
    d = Integer(secrets.randbelow(constants.n - 1) + 1)

    # Compute public key Q
    # At this point, Q is an elliptic curve point (Qx, Qy)
    Q = d * G

    assert not Q.is_zero(), "Public key Q is invalid (point at infinity)"
    assert Q in E, "Public key Q is not on the curve"

    return (d, Q)





def sign(m, d):
    
    """It signs the message m with the private key d

    Returns:
        (r, s): the signature of the message
    """

    # Compute the has of the message
    h = hashlib.sha256(m).digest()

    # Convert hash to integer z
    z = Integer(int.from_bytes(h, 'big'))

    # Truncate to leftmost N bits if hash length > curve bit length
    N = constants.n.nbits()
    hash_len = z.nbits()

    if hash_len > N:
        z = z >> (hash_len - N)
        
    # Let's generate the nonce k
    # Must be random in [1, n-1] per message

    k = R = r = 0

    # Using a while True with break to clone the behaviour of a 
    # do while loop

    r = s = 0
    while True: 
        k = Integer(secrets.randbelow( constants.n - 1 ) + 1 )
        R = k * G #(Rx, Ry)
        r = Integer(R[0]).mod(constants.n)
        
        k_inv = inverse_mod(k, constants.n)
        s = (k_inv * (z + r*d)).mod(constants.n)
        
        if r != 0 and s != 0:
            break
        
    if s > constants.n // 2:
        s = constants.n - s


    return (r, s)


def verify(m, signature, Q):
    """_summary_

    Args:
        m (binary): message to verify
        signature (tuple(r, s)): the signature of the message
        Q (Big Integer): public key

    Returns:
        boolean: True if the signature is valid, False otherwise
    """
    
    r, s = signature
    
    if not (1 <= r < constants.n and 1 <= s < constants.n):
        raise ValueError("Invalid signature values")
    
    h = hashlib.sha256(m).digest()
    z = Integer(int.from_bytes(h, 'big'))
    
    N = constants.n.nbits()
    hash_len = z.nbits()
    
    if hash_len > N:
        z = z >> (hash_len - N)
    
    # Modular inverse of s moulod n
    w = inverse_mod(s, constants.n)
    
    # Let's compute the scalars u1 and u2
    
    u1 = (z * w).mod(constants.n)
    u2 = (r * w).mod(constants.n)
    
    # Compute curve point
    
    X = u1 * G + u2 * Q
    
    if X.is_zero():
        return False
    
    # X is a point on the curve
    # If X is the point at infinity -> invalid signature
    
    v = Integer(X[0]).mod(constants.n)
    
    return v == r

