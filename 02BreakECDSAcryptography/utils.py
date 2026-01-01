import base58
import binascii

def varstr(s):
    if type(s) is str:
        s = s.encode('utf-8')
    length = len(s)
    if length < 0xfd:
        return bytes([length]) + s
    elif length < 0xffff:
        return b'\xfd' + length.to_bytes(2, byteorder='little') + s
    elif length < 0xffffffff:
        return b'\xfe' + length.to_bytes(4, byteorder='little') + s
    else:
        return b'\xff' + length.to_bytes(8, byteorder='little') + s

def base58CheckDecode(s):
    return base58.b58decode_check(s)

def base58decode(s):
    return base58.b58decode(s)

def base256encode(n):
    # This seems to be a big integer to bytes encoding based on usage in keyUtils.py
    # keyUtils: utils.base256encode(utils.base58decode(wallet_private)).encode('hex')
    # But wait, base58decode usually returns bytes in python libraries, or int?
    # Library 'base58' b58decode returns bytes.
    # If n is bytes, return it? usage in keyUtils suggests it might expect something else or it's a no-op shim for py3 bytes.
    # Let's check keyUtils usage: 
    # wallet_key = utils.base256encode(utils.base58decode(wallet_private)).encode('hex')
    # If base58decode returns bytes, base256encode might just be identity or ensuring it's bytes.
    return n

