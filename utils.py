#!/usr/bin/env python

import binascii
import hashlib

from bitcoin.key import CKey as Key
from bitcoin.base58 import encode, decode
from bitcoin.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
from bitcoin.script import OP_VAULT_WITHDRAW, OP_VAULT_CONFIRM, OP_VAULT_OVERRIDE
from bitcoin.script import OP_VAULT_FAST_WITHDRAW


def myhash(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def myhash160(s):
    h = hashlib.new('ripemd160')
    h.update(hashlib.sha256(s).digest())
    return h.digest()


def getnewaddress():
    # Generate public and private keys
    key = Key()
    key.generate()
    key.set_compressed(True)
    private_key = key.get_privkey()
    public_key = key.get_pubkey()
    private_key_hex = private_key.encode('hex')
    public_key_hex = public_key.encode('hex')
    public_key_bytearray = bytearray.fromhex(public_key_hex)
    # Perform SHA-256 and RIPEMD-160 hashing on public key
    hash160_address = myhash160(public_key_bytearray)
    # add version byte: 0x00 for Main Network
    extended_address = '\x00' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    # Convert the result from a byte string into a base58 string using Base58Check encoding.
    address = encode(binary_address)
    return public_key, private_key, address


def public_key_to_address(public_key):
    public_key_hex = public_key.encode('hex')
    public_key_bytearray = bytearray.fromhex(public_key_hex)
    # Perform SHA-256 and RIPEMD-160 hashing on public key
    hash160_address = myhash160(public_key_bytearray)
    # add version byte: 0x00 for Main Network
    extended_address = '\x00' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    address = encode(binary_address)
    return address


def public_key_hex_to_address(public_key_hex):
    public_key_bytearray = bytearray.fromhex(public_key_hex)
    # Perform SHA-256 and RIPEMD-160 hashing on public key
    hash160_address = myhash160(public_key_bytearray)
    # add version byte: 0x00 for Main Network
    extended_address = '\x00' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    address = encode(binary_address)
    return address


def addresses_to_vault_address(address, master_address, timeout):
    timeout = 100 # FIXME: remove hardcoding
    fees = 10000 # FIXME: remove hardcoding
    if timeout > 100:
        timeout = 100
    if fees > 10000:
        fees = 10000
    pubkey_hash_hex = address_to_public_key_hash_hex(address)
    master_pubkey_hash_hex = address_to_public_key_hash_hex(master_address)
    vault_script_hex = pubkey_hash_hex + master_pubkey_hash_hex + hex(timeout)[2:4] + hex(fees)[2:6]
    vault_script_hex_ba = bytearray.fromhex(vault_script_hex)
    hash160_address = myhash160(vault_script_hex_ba)
    # add version byte: 0x08 for vault address
    extended_address = '\x08' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4.
    # This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    # encode in base-58 format
    vault_address = encode(binary_address)
    return str(vault_address)


def addresses_to_vault_script(address, master_address, timeout):
    timeout = 100
    fees = 10000
    if timeout > 100:
        timeout = 100
    if fees > 10000:
        fees = 10000
    pubkey_hash_hex = address_to_public_key_hash_hex(address)
    master_pubkey_hash_hex = address_to_public_key_hash_hex(master_address)
    vault_script_hex = pubkey_hash_hex + master_pubkey_hash_hex + hex(timeout)[2:4] + hex(fees)[2:6]
    vault_script = binascii.unhexlify(vault_script_hex)
    return chr(len(vault_script)) + vault_script


def public_key_to_vault_address(public_key):
    public_key_hex = public_key.encode('hex')
    public_key_bytearray = bytearray.fromhex(public_key_hex)
    # Perform SHA-256 and RIPEMD-160 hashing on public key
    hash160_address = myhash160(public_key_bytearray)
    # add version byte: 0x08 for vault address
    extended_address = '\x08' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    address = encode(binary_address)
    return address


def public_key_hex_to_vault_address(public_key_hex):
    public_key_bytearray = bytearray.fromhex(public_key_hex)
    # Perform SHA-256 and RIPEMD-160 hashing on public key
    hash160_address = myhash160(public_key_bytearray)
    # add version byte: 0x08 for Vault Address
    extended_address = '\x08' + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address.
    binary_address = extended_address + checksum
    address = encode(binary_address)
    return address


def address_to_public_key_hash(address):
    binary_address = decode(address)
    # remove the 4 checksum bytes
    extended_address = binary_address[:-4]
    # remove version byte: 0x00 for Main Network
    hash160_address = extended_address[1:]
    return hash160_address


def address_to_vault_hash(vault_address):
    return address_to_public_key_hash(vault_address)


def address_to_public_key_hash_hex(address):
    binary_address = decode(address)
    # remove the 4 checksum bytes
    extended_address = binary_address[:-4]
    # remove version byte: 0x00 for Main Network
    hash160_address = extended_address[1:]
    public_key_hash_hex = str(binascii.hexlify(hash160_address))
    return public_key_hash_hex


def public_key_hex_to_pay_to_script_hash(public_key_hex):
    script = "41" + public_key_hex + "AC"
    return binascii.unhexlify(script)


def public_key_hex_to_pay_to_pubkey(public_key_hex):
    script = "41" + public_key_hex + "AC"
    return binascii.unhexlify(script)


def public_key_to_pay_to_pubkey(public_key):
    script = "41" + binascii.hexlify(public_key) + "AC"
    return binascii.unhexlify(script)


def address_to_pay_to_pubkey_hash(address):
    pubkey_hash = address_to_public_key_hash(address)
    script = "76A914" + str(binascii.hexlify(pubkey_hash)) + "88AC"
    # script = OP_DUP + OP_HASH160 + pubkey_hash + OP_EQUALVERIFY + OP_CHECKSIG
    return binascii.unhexlify(script)


def public_keys_hex_to_vault_script(public_key_hex, master_public_key_hex, timeout, fees = 0):
    if timeout > 100:
        timeout = 100
    if fees > 10000:
        fees = 10000
    vault_script = public_key_hex + myhash(master_public_key_hex) + hex(timeout)[2:4] + hex(fees)[2:6]
    return vault_script


def public_keys_to_vault_script(public_key, master_public_key, timeout, fees = 0):
    if timeout > 100:
        timeout = 100
    if fees > 10000:
        fees = 10000
    vault_script = public_key.encode('hex') + myhash(master_public_key.encode('hex')) + hex(timeout)[2:4] + hex(fees)[2:6]
    return vault_script


def is_sent_to_vault(scriptPubKey):
    pass


def vault_address_to_pay_to_vault_script(vault_address):
    vault_hash = address_to_vault_hash(vault_address)
    vault_hash_hex = binascii.hexlify(vault_hash)
    # hex: OP_DUP ("76")+ OP_HASH160 ("A9") + hash + OP_EQUAL ("87") + OP_VAULT ("C4")
    pay_to_vault_script_hex = "76" + "A9" + "14" + vault_hash_hex + "87" + "D0"
    pay_to_vault_script = binascii.unhexlify(pay_to_vault_script_hex)
    return pay_to_vault_script


def sriptSig_to_pubkey(script):
    len_signed_data = ord(script[0])
    len_pubkey_data = ord(script[len_signed_data:len_signed_data+1])
    return script[-len_pubkey_data:]


# this is returning hex hash ... fix this
def output_script_to_public_key_hash(script):
    # better matching .. but for now . .. this should work
    if not script:
        return
    # is the script is a standard generation address
    if binascii.hexlify(script[:1]) == "41":
        return binascii.hexlify(myhash160(bytearray.fromhex(binascii.hexlify(script[1:-1]))))
    # is the script is a standard transaction address
    elif binascii.hexlify(script[:3]) == "76a914":
        return binascii.hexlify(script[3:-2])
    elif script[:1] == binascii.unhexlify("14"):
        # hex: "14" (Push 20 bytes) + vault_script_hash + "87" (OP_EQUAL) + "C4" (OP_VAULT)
        return binascii.hexlify(script[1:-2])
    else:
        raise Exception("Error unknown scritpt: ", binascii.hexlify(script))
    return None


def output_script_to_address(script):
    version = '0x00'
    if script[:1] == binascii.unhexlify("41"):
        version = binascii.unhexlify('00')
    elif script[:1] == binascii.unhexlify("76"):
        version = binascii.unhexlify('00')
    elif script[:1] == binascii.unhexlify("14"):
        version = binascii.unhexlify('08')
    else:
        raise Exception("Error unknown scritpt: ", binascii.hexlify(script))
    # fix this into a single complete module
    hash160_address = binascii.unhexlify(output_script_to_public_key_hash(script))
    # add version byte: 0x00 for Main Network
    extended_address = version + hash160_address
    # generate double SHA-256 hash of extended address
    hash_address = myhash(extended_address)
    # Take the first 4 bytes of the second SHA-256 hash. This is the address checksum
    checksum = hash_address[:4]
    # Add the 4 checksum bytes from point 7 at the end of extended RIPEMD-160 hash from point 4. This is the 25-byte binary Bitcoin Address
    binary_address = extended_address + checksum
    # encode in base 58 format
    address = encode(binary_address)
    return address


def scriptPubKey_to_pubkey_hash(scriptPubkey):
    if not scriptPubkey:
        return None
    # is the script is a standard generation address
    if scriptPubkey[:1] == binascii.unhexlify("41"):
        return myhash160(bytearray.fromhex(binascii.hexlify(scriptPubkey[1:-1])))
    # is the script is a standard transaction address
    elif scriptPubkey[:3] == binascii.unhexlify("76a914"):
        return scriptPubkey[3:-2]
    elif scriptPubkey[:1] == binascii.unhexlify("14"):
        # hex: "14" (Push 20 bytes) + vault_script_hash + "87" (OP_EQUAL) + "C4" (OP_VAULT)
        return scriptPubkey[1:-2]
    else:
        raise Exception("Error unknown scritpt: ", binascii.hexlify(scriptPubkey))
    return None


def scriptSig_to_address(scriptSig):
    if not scriptSig:
        return None
    elif ord(scriptSig[0]) in [OP_VAULT_WITHDRAW, OP_VAULT_FAST_WITHDRAW, \
        OP_VAULT_CONFIRM]:
        return scriptSig_to_vault_address(scriptSig)
    else:
        public_key = sriptSig_to_pubkey(scriptSig)
        return public_key_to_address(public_key)


def scriptSig_to_public_key_hash(script):
    if not script:
        return
    # remove the signature
    signature_length = ord(script[:1])
    script = script[1 + signature_length:]
    # remove pubkey length and return
    return script [1:]


def is_sent_from_vault(scriptSig):
    if not scriptSig:
        return False
    if ord(scriptSig[0]) in [OP_VAULT_FAST_WITHDRAW, OP_VAULT_CONFIRM]:
        return True
    return False

# Move this code in to tx itself is_vault_tx()
def is_vault_tx(tx):
    if tx.is_coinbase():
        return False
    if len(tx.vin) != 1:
        return False
    scriptSig = tx.vin[0].scriptSig
    if ord(scriptSig[0]) in [OP_VAULT_WITHDRAW, OP_VAULT_CONFIRM, \
        OP_VAULT_OVERRIDE]:
        return True
    return False

def scriptSig_to_vault_address(scriptSig):
    if not scriptSig:
        return None
    if ord(scriptSig[0]) not in [OP_VAULT_WITHDRAW, OP_VAULT_FAST_WITHDRAW, \
        OP_VAULT_CONFIRM]:
        return None
    key_type = scriptSig[0]
    start_index = 0
    # skip the vault withdraw type
    start_index = start_index + 1
    # skip the master key
    if key_type == chr(OP_VAULT_FAST_WITHDRAW):
        # skip the master key
        start_index = start_index + ord(scriptSig[start_index]) + 1
    # skip the signature
    start_index = start_index + ord(scriptSig[start_index]) + 1
    # get script length
    script_length = ord(scriptSig[start_index])
    # skip the script length
    start_index = start_index + 1
    # calculate the end index
    end_index = start_index + script_length
    # get the from address
    # vault_address = vault_address_to_pay_to_vault_script(
    vault_address = public_key_to_vault_address( \
        scriptSig[start_index:end_index])

    return vault_address


"""
# Output script to address representation
def script_to_address(script,vbyte=0):
    if re.match('^[0-9a-fA-F]*$',script):
        script = script.decode('hex')
    if script[:3] == '\x76\xa9\x14' and script[-2:] == '\x88\xac' and len(script) == 25:
        return bin_to_b58check(script[3:-2],vbyte) # pubkey hash addresses
    else:
        return bin_to_b58check(script[2:-1],5) # BIP0016 scripthash addresses

def p2sh_scriptaddr(script):
    if re.match('^[0-9a-fA-F]*$',script): script = script.decode('hex')
    return hex_to_b58check(hash160(script),5)
"""


def mk_pubkey_script(addr): # Keep the auxiliary functions around for altcoins' sake
    return '76a914' + b58check_to_hex(addr) + '88ac'


def mk_scripthash_script(addr):
    return 'a914' + b58check_to_hex(addr) + '87'


# Address representation to output script
def address_to_script(addr):
    if addr[0] == '3': return mk_scripthash_script(addr)
    else: return mk_pubkey_script(addr)


# FIX ME: fees is not fixed, but for now its isset to 1
def calculate_fees(tx):
    return 1
