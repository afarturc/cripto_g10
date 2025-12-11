from collections import namedtuple
from sage.all import Integer
# Let's first create as inmmutable constants, the values for
# the curve P-192

# This is a whim of mine (Fábio) not something necessary.
# I like not having the fear of changing something I shouldn't

Constants = namedtuple("Constants", ["p", "a", "n", "SEED", "c", "b", "Gx", "Gy", "h"])

P = Integer(6277101735386680763835789423207666416083908700390324961279)

# a = p - 3 because for all the prime curves, the equation
# that defines them is y^2 = x^3 - 3x + b
# so a = -3 mod p which is the same as a = p - 3


constants = Constants(
    p = P,
    a = Integer(P - 3),
    n = Integer(6277101735386680763835789423176059013767194773182842284081),
    SEED = Integer(0x3045ae6fc8422f64ed579528d38120eae12196d5),
    c = Integer(0x3099d2bbbfcb2538542dcd5fb078b6ef5f3d6fe2c745de65),
    b = Integer(0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1),
    Gx = Integer(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012),
    Gy = Integer(0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811),
    h = 1
)
