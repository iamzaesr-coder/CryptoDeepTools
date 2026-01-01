import sys
import bitcoin
from Crypto.Hash import SHA256
import txnUtils
import keyUtils
import binascii

# tx = ""
# In python 3, sys.argv[1] is a string. If we want bytes, we might need to handle it.
# usage: python breakECDSA.py <hex_string>
# So tx will be a hex string.
if len(sys.argv) > 1:
    tx = sys.argv[1]
else:
    print("Usage: python breakECDSA.py <hex_tx>")
    sys.exit(1)

# Parse the transaction
# parseTxn expects a hex string? 
# In txnUtils.py: parseTxn(txn) -> access by index, string slicing.
# txn[0:41*2] ...
# So txn should be a hex string.
m = txnUtils.parseTxn(tx)
e = txnUtils.getSignableTxn(m)

# Calculate the double SHA-256 hash
# getSignableTxn returns hex string.
# SHA256.new expects bytes in Py3.
hash1 = SHA256.new(bytes.fromhex(e)).digest()
hash2 = SHA256.new(hash1).digest()

# Convert to hex and reverse for signature processing
# hash2 is bytes. [::-1] on bytes works. .hex() works.
z1 = hash2[::-1].hex()
z = hash2.hex()

# Get the signature and public key
# m[1] is sig (hex string).
s = keyUtils.derSigToHexSig(m[1][:-2])
pub = m[2]
sigR = s[:64]
sigS = s[-64:]
sigZ = z

# Print results
print("R = 0x" + sigR)
print("S = 0x" + sigS)
print("Z = 0x" + sigZ)
print("")
print("PUBKEY = " + pub)
print("")
print("======================================================================")
print("")
