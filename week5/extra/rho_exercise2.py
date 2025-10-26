"""
Rho method para encontrar colisões de hash

Ideia: aplicar H repetidamente cria uma estrutura tipo ρ (cauda + ciclo)
A colisão está onde a cauda encontra o ciclo

Algoritmo:
1. Detetar ciclo com tartaruga (1 passo) e lebre (2 passos)
2. Encontrar início do ciclo
3. Extrair os dois valores que colidem
"""

from cryptography.hazmat.primitives import hashes
import os
import time

L = 5

def H(X):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(X)
    return (digest.finalize()[0:L])

def rho(h0):
    print("Hash is "+str(8*L)+" bits")
    
    # Fase 1: detetar ciclo
    slow = h0
    fast = h0
    iterations = 0
    
    while True:
        slow = H(slow)
        fast = H(H(fast))
        iterations += 1
        if slow == fast:
            break
    
    # Fase 2: encontrar início do ciclo
    slow = h0
    prev = None
    mu = 0
    
    while slow != fast:
        prev = slow
        slow = H(slow)
        fast = H(fast)
        mu += 1
    
    cycle_start = slow
    
    # Fase 3: encontrar predecessor no ciclo
    current = cycle_start
    cycle_len = 1
    temp = H(current)
    
    while temp != cycle_start:
        current = temp
        temp = H(current)
        cycle_len += 1
    
    print(f"Iterações: {iterations}, μ={mu}, λ={cycle_len}")
    
    hi = current
    return (prev, hi)

# Execução
start = os.urandom(L)
print(f"Início: {start.hex()}\n")

t0 = time.time()
(h0, h1) = rho(start)
t1 = time.time()

print(f"\nColisão encontrada:")
print(f"  {h0.hex()}")
print(f"  {h1.hex()}")
print(f"\nH(v1) = {H(h0).hex()}")
print(f"H(v2) = {H(h1).hex()}")

if H(h0) == H(h1):
    print("\nVerificado!")

print(f"\nTempo: {t1-t0:.2f}s")

# Análise de escalamento
print(f"\nComplexidade esperada: ~2^(n/2) = 2^{4*L} = {2**(4*L)} ops")
print("Escalamento: L+1 → tempo x16")