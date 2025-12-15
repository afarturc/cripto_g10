# Extra week #11

## Q1: Demonstrating forgeability of plain RSA

The attacker will request the signatures of the messages $m_{1}$ and $m_{2}b$. Such that $m_{1}m_{2} \equiv 1\pmod n$

So this way we have:

$s_{1} = (m_{1})^{d}$ and $s_{2} = (m_{2}b)^{d}$

If we multiply $s_{1}$ and $s_{2}$ we get

$s_{1} \cdot s_{2} \mod n = (m_{1})^{d} \cdot (m_{2}b)^{d} \mod n = (m_{1} \cdot m_{2}b)^{d} \mod n = (1 \cdot b)^d \mod n = b^d \mod n$

Since a signature for a message $m$ is $m^d$, we forged a valid signature for $b$, which is $b^d$


## Q2: Shamir Secret Sharing

### Question - P1
#### 1)

The degree of the polynomial should be 2. With only 2 points, we can only reconstruct a polynomial of at most degree 1.

With 3 points though, we can reconstruct a polynomial of degree 2 with the **Lagrange Polynomial**.

We will create three "mini-parables" for 3 different points.

We will then create three polynomials for each point so that for the chosen point, the given result will be 1 and for the others the result will be 0.

For three arbitraty points $P_{1} = (x_{1}, y_{1})$, $P_{2} = (x_{2}, y_{2})$ , $P_{3} = (x_{3}, y_{3})$. The correspondent Lagrange for polynomial $L_{P_{1}}(x)$ would be:

$L_{P_{1}}(x) = \frac{(x-x_{2})(x-x_{3})}{(x_{1}-x_{2})(x_{1}-x_{3})}$

At the end, the equation for the secret would be:

$P(x) = y_{1} \times L_{1}(x) + y_{2} \times L_{2}(x)+ y_{3} \times L_{3}(x)$

#### 2)
We construct the polynomial as:

$f(t) = a_0 + a_1 \cdot t + a_2 \cdot t^2$

Where:
- $a_0 = x$ (the secret)
- $a_1$ = random integer coefficient
- $a_2$ = random integer coefficient (non-zero to ensure degree 2)

**Why this works:**

When we evaluate at $t = 0$:

$f(0) = a_0 + a_1 \cdot 0 + a_2 \cdot 0^2 = a_0 = x$

**Example:**
If the secret is $x = 42$, and we randomly choose $a_1 = 5$ and $a_2 = 3$:

$f(t) = 42 + 5t + 3t^2$

Verification: $f(0) = 42 + 5(0) + 3(0)^2 = 42$ ✓

**Generating the shares:**
We then evaluate this polynomial at different points to create the shares:
- Share 1: $(1, f(1)) = (1, 50)$
- Share 2: $(2, f(2)) = (2, 64)$
- Share 3: $(3, f(3)) = (3, 84)$
- Share 4: $(4, f(4)) = (4, 110)$


### Question - P2

The implementation of what was asked is on the file **answers_extra/Q2_P2.py**
