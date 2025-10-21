from cryptography.hazmat.primitives import hashes
from binascii import hexlify, unhexlify
import os
import numpy as np

# The most common passwords of 2019.
passwds = ['123456','123456789','qwerty','password','1234567','12345678','12345','iloveyou','111111','123123','abc123','qwerty123','1q2w3e4r','admin','qwertyuiop','654321','555555','lovely','7777777','welcome']

### Non-salt version

# Get their hex versions
hex_passwds = []
for pwd in passwds:
	hex_passwds.append(hexlify(pwd.encode()))

# Hash all the passwords
hlist = []
for pwd in hex_passwds:
	digest = hashes.Hash(hashes.SHA256())
	digest.update(pwd)
	hlist.append(hexlify(digest.finalize()))

#### Salt version

# Random salt of 1 byte
salt_passwds = []
salt = os.urandom(1)

# The same passwords, but now with the random salt prepended
for pwd in hex_passwds:
	salt_passwds.append(salt+pwd)

# Hash all salted passwords
shlist = []
for pwd in salt_passwds:
	digest = hashes.Hash(hashes.SHA256())
	digest.update(pwd)
	shlist.append(hexlify(digest.finalize()))

### Lets mix it up
# numpy 1.5.0 required!
mixed_hlist = np.random.permutation(hlist)
mixed_shlist = np.random.permutation(shlist)

### Exercise 1 - Crack unsalted hashes
# Show that it is trivial to take a set of hashed passwords and know their corresponding passwords, with knowledge of "good" candidates
# Take "mixed_hlist" (a shuffled version of password hashes) and "hex_passwds" (the hexlify list of candidates) and produce a list of "cracked_pwds". This should be a decoding of "mixed_hlist": for each hash in "mixed_hlist", "cracked_pwds" should have its original password.
## Important! ## Do not use any other information. That is cheating :-)  

cracked_pwds = [0 for _ in range(len(mixed_hlist))]


		# Your code here!!
  
def break_hashes(hex_passwds, mixed_hlist, cracked_pwds):  
	for passwd in hex_passwds:
		digest = hashes.Hash(hashes.SHA256())
		digest.update(passwd)
		hashed_passwd_final = hexlify(digest.finalize())
	
		for j in range(len(mixed_hlist)):
		
			if hashed_passwd_final == mixed_hlist[j]:
		
				cracked_pwds[j] = passwd

break_hashes(hex_passwds, mixed_hlist, cracked_pwds)
# Lets see if your list is correct

print("Checking non-salted cracked passwords:")

i = 0
for pwd in cracked_pwds:
	digest = hashes.Hash(hashes.SHA256())
	digest.update(pwd)
	if (mixed_hlist[i] == hexlify(digest.finalize())):
		print(i, "Check")
	i += 1

### Exercise 2 - Crack salted hashes
# Now we show that salting makes it more challenging, but it is still doable. The scenario is still quite simple: each password was hashed with a small salt (but all of them with the same one!). Can you do the same thing?
# Take "mixed_shlist" (a shuffled version of password salted hashes) and "hex_passwds" (the hexlify list of candidates) and produce a list of "cracked_pwds". This should be a decoding of "mixed_hlist": for each hash in "mixed_hlist", "cracked_pwds" should have its original password.
## Important! ## Do not use any other information. That is still cheating :-)  


## STUDENT COMMENT ##

##Let's find the salt first. We know that the salt is one byte long, so we can try all 256 possibilities for one of the hashes.

cracked_spwds = []

		# Your code here!!

def find_salt(shlist, hex_passwds):
	found_salt = None
	for salt in range(256):
		salt_byte = bytes([salt])
	
		first_salted_hashed = shlist[0]
	
		digest = hashes.Hash(hashes.SHA256())
		digest.update(salt_byte + hex_passwds[0])
		hashed_passwd_final = hexlify(digest.finalize())
	
		if hashed_passwd_final == first_salted_hashed:
			found_salt = salt_byte
			break

	return found_salt

found_salt = find_salt(shlist, hex_passwds)
print(f"Found salt: {found_salt}")


cracked_spwds = [0 for _ in range(len(mixed_shlist))]

def break_salted_hashes(hex_passwds, mixed_shlist, cracked_spwds):
	salt = find_salt(mixed_shlist, hex_passwds)
  
	#Let's reuse the previous function with the found salt
	break_hashes(salt_passwds, mixed_shlist, cracked_spwds)
 
break_salted_hashes(hex_passwds, mixed_shlist, cracked_spwds)
	
print("Checking salted cracked passwords:") 
 
i = 0
for pwd in cracked_spwds:
	digest = hashes.Hash(hashes.SHA256())
	digest.update(pwd)
	if (mixed_shlist[i] == hexlify(digest.finalize())):
		print(i, "Check")
	i += 1
