from pwn import *

config_alice = "config_alice"
config_bob = "config_bob"

def readFileConfig(filename):
    """Reads the configuration file given

    Args:
        filename (string): the name of the configuration file
    
    Returns:
        tuple: the host and the port (host, port)
    """
    f = open(filename, "r")
    host = f.readline()[:-1]
    port = int(f.readline())
    f.close()
    
    return (host, port)

hostAlice, portAlice = readFileConfig(config_bob)
hostBob, portBob = readFileConfig(config_alice)

g = 2
p = 7853799659

# Connecting to Alice
r_alice = remote(hostAlice, portAlice)
l_alice = listen(portBob)
l_alice.wait_for_connection()

x = random.randint(1, p)
y = random.randint(1, p)

# gy will be the one sent to Alice
gy_alice = pow(g, y, p)

# gx will be the one sent to Bob
gx_bob = pow(g, x, p) 

print("Sending GY to Alice: ", gy_alice)
r_alice.sendline(gy_alice.to_bytes(8, "little"))

gx_alice = int.from_bytes(l_alice.recvline()[:-1], "little")
print("Received GX from Alice:", gx_alice)

l_alice.close()
r_alice.close()

# Connecting to Bob
l_bob = listen(portAlice)
l_bob.wait_for_connection()
r_bob = remote(hostBob, portBob)

gy_bob = int.from_bytes(l_bob.recvline()[:-1], "little")
print("Received GY from Bob:", gy_bob)

print("Sending GX to Bob: ", gx_bob)
r_bob.sendline(gx_bob.to_bytes(8, "little"))

l_bob.close()
r_bob.close()

print(f"Shared secret with Bob: {pow(gy_bob, x, p)}")
print(f"Shared secret with Alice: {pow(gx_alice, y, p)}")










