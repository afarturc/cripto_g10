import os

encryption_key = os.urandom(16) # generates 16 bytes = 128 bits
authentication_key = os.urandom(32) # generates 32 bytees = 256 bits

with open("pw", "wb") as f:
    f.write(encryption_key)
    f.write(authentication_key)
    
print("Keys generated and saved to 'pw'")

