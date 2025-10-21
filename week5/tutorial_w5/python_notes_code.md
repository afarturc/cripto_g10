## README: SHA-256 length-extension attack (Lab Q4)

This lab demonstrates a length-extension attack against an insecure MAC construction that hashes `key || message` with SHA-256. The attacker forges a new message m′ and tag h′ such that `SHA256(key || m′) = h′` without knowing the secret key.

### What changed (fixes applied)
- Continue the hash from the original digest (digest-as-IV) over only the attacker’s extension bytes.
- Account for all bytes already processed by the server when building the forged tag: `prefix_len = key_len + len(original_msg) + len(glue_padding)`.
- Verify the forged tag properly with `SHA256(key || forged_message)` and write artifacts to `outputs/`.

### Files of interest
- `answer/question4/generator_q4.py` — generates a random key, the original message, and its tag; writes `outputs/key.bin`, `outputs/message.bin`, `outputs/tag.bin`.
- `answer/question4/sha_implementation.py` — pure-Python SHA-256 that supports custom IV and prefix length (used to resume hashing).
- `answer/question4/attacker_q4.py` — performs the length-extension attack; writes `outputs/forged_message.bin`, `outputs/forged_tag.bin`.

### How the attack works (SHA-256 specifics)
1) The server computes `h = SHA256(key || m)` and publishes `(m, h)`.
2) The attacker chooses an extension `ext` and computes the “glue padding” that SHA-256 would add after `key || m`.
3) The attacker forges `m′ = m || glue || ext` and resumes SHA-256 from the internal state encoded in `h`, with the bit counter set to reflect the total processed bytes so far.
4) The result is `h′ = SHA256(key || m′)` — a valid tag for a different message.

Key detail: the glue padding and internal bit counter depend on the total bytes before the extension, i.e., `key_len + len(m)`. If key length isn’t known, the attacker tries a small plausible range (e.g., 8–64).

### Why it was failing before
- The attack hashed `original || glue || extension` again starting from the digest as IV. That re-hashed original bytes under a non-standard IV.
- It didn’t advance the internal length by the glue padding, so the SHA-256 bit counter didn’t match the server’s state.
- Verification compared against `SHA256(key || original || extension)` instead of `SHA256(key || original || glue || extension)`.

### What the fixed code does
- Builds `m′ = m || glue || ext` for each `key_len` guess.
- Computes `h′` by hashing only `ext` while seeding the SHA-256 state with `h` and using `prefix_len = key_len + len(m) + len(glue)`.
- Verifies locally with the hidden `key.bin` (lab-only) and writes:
	- `outputs/forged_message.bin` (m′)
	- `outputs/forged_tag.bin` (h′)

### How to run
```bash
# 1) Generate original artifacts
python3 answer/question4/generator_q4.py

# 2) Run the attacker (tries key lengths 8..64, stops on success)
python3 answer/question4/attacker_q4.py
```

Expected console output (example):
```
Trying key length: 8
...
Trying key length: 32
Success! Key length guessed: 32
Forged tag: 81f5d5f1a2f91f9f80e24db2e61863474ec459a2d2b9d1c31710586f28a66156
New message length: 45 bytes
```

Artifacts written:
- `outputs/forged_message.bin` — the forged message `m′ = m || glue || ext`
- `outputs/forged_tag.bin` — the forged tag `h′`

### Notes and caveats
- The attacker doesn’t know the key bytes; only the length is needed to compute correct padding. In a real attack, you would try a small range and use a server oracle to tell which candidate is accepted.
- The glue padding is binary (starts with `0x80`, followed by zeros, then an 8-byte big-endian length). Protocols that treat messages as ASCII may make the attack impractical.
- HMAC-SHA256 is not vulnerable to length extension. This attack applies to raw prefix-MACs like `SHA256(key || msg)`.

### Troubleshooting
- No success after trying all lengths:
	- Confirm the generator uses a prefix-MAC (not HMAC).
	- Ensure `attacker_q4.py` reads `outputs/message.bin` and `outputs/tag.bin` from the same run of the generator.
	- If you removed `outputs/key.bin`, verification can’t occur; the attacker will still write candidate forged outputs.
- Import errors for extra libraries: this solution uses only the included `sha_implementation.py` and standard libraries; no external packages are required.

### Summary
With the corrected continuation logic (digest-as-IV + accurate prefix bit count), the attacker successfully forges a valid `(m′, h′)` such that `SHA256(key || m′) = h′`, demonstrating the length-extension vulnerability of raw SHA-256 prefix-MACs.

