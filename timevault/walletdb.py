#!/usr/bin/env python

import os
import sqlite3
import logging
from bsddb.db import *
from pickle import dumps, loads

import binascii
from bitcoin import script
from bitcoin.key import CKey
from bitcoin.core import COutPoint, CTxIn, CTxOut, CTransaction
from bitcoin.script import OP_VAULT_WITHDRAW, OP_VAULT_FAST_WITHDRAW, OP_VAULT_CONFIRM, OP_VAULT_OVERRIDE

# Joric/bitcoin-dev, june 2012, public domain
import hashlib
import ctypes
import ctypes.util
import sys
import utils
#import base58


"""
walletdb: wallet data structure
    accounts: list of accounts
        account: the default account
            subaccount:
                address: address
                public_key: public_key
                private_key: private_key
                balance: 0.0
                height: 0
                received : [transactions]
    vaults: list of vaults
        vault:
            name: name of the vault
            address: address of primary key
            master_address: address of master key
            amount: amount held by this vault
            fees: max fees associated with this vault

Note:
    For EC keys, don't use secret based key generation.
    Only use the keys in default form (No compress or uncompress)
"""

ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('ssl') or 'libeay32')
ssl.EC_KEY_new_by_curve_name.restype = ctypes.c_void_p

def check_result (val, func, args):
    if val == 0: raise ValueError
    else: return ctypes.c_void_p (val)


ssl.EC_KEY_new_by_curve_name.errcheck = check_result

"""
refactor the base58 functions and module to bitcoin lib
"""

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(n):
    l = []
    while n > 0:
        n, r = divmod(n, 58)
        l.insert(0,(b58_digits[r]))
    return ''.join(l)

def base58_decode(s):
    n = 0
    for ch in s:
        n *= 58
        digit = b58_digits.index(ch)
        n += digit
    return n

def base58_encode_padded(s):
    res = base58_encode(int('0x' + s.encode('hex'), 16))
    pad = 0
    for c in s:
        if c == chr(0):
            pad += 1
        else:
            break
    return b58_digits[0] * pad + res

def base58_decode_padded(s):
    pad = 0
    for c in s:
        if c == b58_digits[0]:
            pad += 1
        else:
            break
    h = '%x' % base58_decode(s)
    if len(h) % 2:
        h = '0' + h
    res = h.decode('hex')
    return chr(0) * pad + res

def base58_check_encode(s, version=0):
    vs = chr(version) + s
    check = dhash(vs)[:4]
    return base58_encode_padded(vs + check)

def base58_check_decode(s, version=0):
    k = base58_decode_padded(s)
    v0, data, check0 = k[0], k[1:-4], k[-4:]
    check1 = dhash(v0 + data)[:4]
    if check0 != check1:
        raise BaseException('checksum error')
    if version != ord(v0):
        raise BaseException('version mismatch')
    return data

def dhash(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def rhash(s):
    h1 = hashlib.new('ripemd160')
    h1.update(hashlib.sha256(s).digest())
    return h1.digest()

"""
def get_addr(k, version=0):
    pubkey = k.get_pubkey()
    privkey = k.get_privkey()
    hash160 = rhash(pubkey)
    addr = base58_check_encode(hash160, version)
    return addr, binascii.hexlify(privkey), binascii.hexlify(pubkey)
"""

def pubkey_to_address(pubkey, version=0):
    hash160 = rhash(pubkey)
    return base58_check_encode(hash160, version)

def gen_eckey(passphrase=None, secret=None, pkey=None, compressed=False, rounds=1, version=0):
    k = CKey()
    if passphrase:
        secret = passphrase.encode('utf8')
        for i in xrange(rounds):
            secret = hashlib.sha256(secret).digest()
    if pkey:
        secret = base58_check_decode(pkey, 128+version)
        compressed = len(secret) == 33
        secret = secret[0:32]
    k.generate(secret)
    k.set_compressed(compressed)
    return k

# Wallet class
class WalletDB(object):
    def __init__(self, walletfile = "~/.bitcoinpy/wallet.dat"):
        self.walletfile = os.path.expanduser(walletfile)
        self.walletdir = os.path.split(self.walletfile)[0]
        self.db_env = DBEnv(0)
        self.db_env.open(self.walletdir, (DB_CREATE|DB_INIT_LOCK|DB_INIT_LOG|DB_INIT_MPOOL|DB_INIT_TXN|DB_THREAD|DB_RECOVER))
        self.initialize()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    # open wallet database
    def open(self, writable=False):
	    db = DB(self.db_env)
	    if writable:
		    DB_TYPEOPEN = DB_CREATE
	    else:
		    DB_TYPEOPEN = DB_RDONLY
	    flags = DB_THREAD | DB_TYPEOPEN
	    try:
		    r = db.open(self.walletfile, "main", DB_BTREE, flags)
	    except DBError:
		    r = True
	    if r is not None:
		    logging.error("Couldn't open wallet.dat/main. Try quitting Bitcoin and running this again.")
		    sys.exit(1)
	    return db

    def get(self, key):
        key = str(key)
        walletdb = self.open()
        if not key in walletdb:
            self.logger.error("Walletdb: key error")
        value = loads(walletdb[key])
        walletdb.close()
        return value

    def set(self, key, value):
        walletdb = self.open(writable = True)
        walletdb[key] = dumps(value)
        walletdb.sync()
        walletdb.close()


    # if wallet does not exist, create it
    def initialize(self):
        if not os.path.isfile(self.walletfile):
            walletdb = self.open(writable = True)
            # if wallet is not initialized, return
            if 'accounts' in walletdb:
                walletdb.close()
                self.logger.warning("Wallet is already initialized!")
                return None
            subaccount = self.getnewsubaccount()
            walletdb['account'] = dumps({subaccount['address']: subaccount})
            walletdb['accounts'] = dumps(['account'])
            walletdb['vaults'] = dumps([])
            walletdb.sync()
            walletdb.close()
        # create sqlitedb
        connection = sqlite3.connect('vault.db')
        cursor = connection.cursor()
        # FIXME: should be executed only once
        # cursor.execute('''CREATE TABLE vaults (txhash varchar(50), date text)''')
        connection.commit()
        connection.close()


    # return an account
    def getaccount(self, accountname = None):
        accountname = "account"
        walletdb = self.open()
        # if wallet is not initialized, return
        if 'accounts' not in walletdb:
            walletdb.close()
            self.logger.error("Wallet not initialized ... quitting!")
            return None
        # if wallet is initialized
        accountnames = loads(walletdb['accounts'])
        if accountname not in accountnames:
            self.logger.warning("Error: Account not found")
            return
        # if account is in wallet
        account = loads(walletdb[accountname])
        walletdb.close()
        for subaccount in account.itervalues():
            subaccount['balance'] = self.chaindb.getbalance(subaccount['address'])
            subaccount['received'] = self.chaindb.listreceivedbyaddress(subaccount['address']).values()
        return account


    # getaccounts
    def getaccounts(self):
        accounts = []
        walletdb = self.open()
        # if wallet is not initialized, return
        if 'accounts' not in walletdb:
            self.logger.error("Wallet not initialized ... quitting!")
            return None
        # wallet is initialized
        accountnames = loads(walletdb['accounts'])
        for accountname in accountnames:
            account = loads(walletdb[accountname])
            accounts.append(account)
        walletdb.close()

        for account in accounts:
            for address, subaccount in account.iteritems():
                subaccount['balance'] = self.chaindb.getbalance(subaccount['address'])
                subaccount['received'] = self.chaindb.listreceivedbyaddress(
                    subaccount['address']).values()

        return accounts


    # getvaults
    def getvaults(self):
        vaultaccounts = []
        walletdb = self.open()
        # if wallet is not initialized, return
        if 'accounts' not in walletdb:
            self.logger.error("Wallet not initialized ... quitting!")
            return None
        # wallet is initialized
        vaults = loads(walletdb['vaults'])
        for vault in vaults:
            vaultaccount = loads(walletdb[vault])
            vaultaccounts.append(vaultaccount)
        walletdb.close()

        """
        vault = {'name' : vault_name,
                 'address': address, 'public_key': public_key, 'private_key': private_key,
                 'master_address': master_address, 'master_public_key': master_public_key,
                 'master_private_key': master_private_key, 'amount': amount, 'fees': fees}
        """

        #FIXME: format vault accounts in same form as general accounts
        accounts = {}
        for vaultaccount in vaultaccounts:
            subaccount = {}
            subaccount ['address'] = vaultaccount['name']
            subaccount['pubkey'] = vaultaccount['public_key']
            subaccount['privkey'] = vaultaccount['private_key']
            subaccount['height'] = 0
            #subaccount['balance'] = self.chaindb.getsavings(vault)
            #subaccount['balance'] = vaultaccount['amount']
            subaccount['balance'] = self.chaindb.getsavings(vaultaccount['name'])
            subaccount['received'] = self.chaindb.listreceivedbyvault(vault).values()
            accounts[vaultaccount['name']] = subaccount
        return accounts


    # helper functions
    def getnewsubaccount(self):
        key = CKey()
        key.generate()
        private_key = key.get_privkey()
        public_key = key.get_pubkey()
        address = pubkey_to_address(public_key)
        return {"address": address, "public_key": public_key, "private_key": private_key, "balance": 0.0, 'height' : 0, 'received' : []}

    # create and return a new address
    def getnewaddress(self, accountname = None):
        if not accountname:
            accountname = "account"
        walletdb = self.open(writable = True)
        # if wallet is not initialized
        if 'accounts' not in walletdb:
            self.logger.error("Wallet not initialized ... quitting!")
            return None
        # if wallet is initialized
        subaccount = self.getnewsubaccount()
        accountnames = loads(walletdb['accounts'])
        self.logger.debug("account names: %s" % accountnames)
        if accountname in accountnames:
            account = loads(walletdb[accountname])
            account[subaccount['address']] = subaccount
        else:
            self.logger.debug("account: %s not in accounts" % accountname)
            self.logger.debug("creating new account")
            account = {subaccount['address']: subaccount}
            # add the new account name to account names
            walletdb['accounts'] = dumps(accountnames.append(accountname))
        walletdb[accountname] = dumps(account)
        walletdb.sync()
        walletdb.close()
        return subaccount['public_key'], subaccount['address']

    # return balance of an account
    def getbalance(self, accountname):
        if not accountname:
            accountname = "account"
        walletdb = self.open()
        # if wallet is not initialized, return:
        # FIXME: refactor is wallet initialized
        if 'accounts' not in walletdb:
            self.logger.error("Wallet not initialized ... quitting!")
            return None
        # if wallet is initialized
        accountnames = loads(walletdb['accounts'])
        if accountname not in accountnames:
            self.logger.error("Error: Account not found")
            return
        # if account is in wallet
        account = loads(walletdb['account']) # FIXME: account = loads(walletdb[accountname])
        walletdb.close()
        for address, subaccount in account.iteritems():
            transactions = self.chaindb.listreceivedbyaddress(subaccount['address'])
            subaccount['balance'] = 0
            self.logger.debug("Transactions: %r" % transactions)
            for transaction in transactions.itervalues():
                self.logger.debug("Transaction: %r" % transaction)
                subaccount['balance'] = subaccount['balance'] + transaction['value']
            subaccount['received'] = transactions
        return account

    # vault functions
    # create a new vault
    def newvault(self, vault_name, address, master_address, amount, fees = 100):
        account = self.getaccount()
        for subaccount in account:
            if subaccount == address:
                public_key = account[subaccount]['public_key']
                private_key = account[subaccount]['private_key']
            if subaccount == master_address:
                master_public_key = account[subaccount]['public_key']
                master_private_key = account[subaccount]['private_key']
        # open wallet
        walletdb = self.open(writable = True)
        vault = {'name' : vault_name,
                 'address': address, 'public_key': public_key, 'private_key': private_key,
                 'master_address': master_address, 'master_public_key': master_public_key,
                 'master_private_key': master_private_key, 'amount': amount, 'fees': fees}
        walletdb[vault_name] = dumps(vault)
        vaults = loads(walletdb['vaults'])
        vaults.append(vault_name)
        walletdb['vaults'] = dumps(vaults)
        walletdb.sync()
        walletdb.close()

    # return a vault
    def getvault(self, vaultname = None):
        self.logger.debug("Vaultname: %r %r" % (type(vaultname), vaultname))
        walletdb = self.open()
        if not vaultname:
            vaultname = loads(walletdb['vaults'])[0]
        vault = loads(walletdb[str(vaultname)])
        walletdb.close()
        return vault

    # delete a vault
    def deletevault(self, vault_name):
        pass

    # add vault received
    def receivevault(self, vault, txhash):
        pass

    # possible script signatures for a vault
    def scriptSigs(self, vaultaddress):
        vault = self.getvault(vaultaddress)
        master_public_key = vault['master_public_key']
        master_private_key = vault['master_private_key']
        # scriptSig = chr(len(public_key)) + public_key
        masterScriptSig = chr(len(vault['master_public_key'])) + vault['master_public_key']
        """
        self.logger.debug("########### Adding signature: ", binascii.hexlify(masterScriptSig))
        public_key = vault['public_key']
        private_key = vault['private_key'])
        # scriptSig = chr(len(public_key)) + public_key
        masterScriptSig = chr(len(vault['master_public_key'])) + vault['master_public_key']
        self.logger.debug("Adding signature: ", binascii.hexlify(scriptSig))
        """
        return [masterScriptSig]


    # send to an address
    def sendtoaddress(self, toaddress, amount):
        # select the input addresses
        funds = 0
        subaccounts = []
        accounts = self.getaccounts()
        for account in accounts:
            for address, subaccount in account.iteritems():
                if subaccount['balance'] == 0:
                    continue
                else:
                    subaccounts.append(subaccount)
                    funds = funds + subaccount['balance']
                    if funds >= amount + utils.calculate_fees(None):
                        break

        # incase of insufficient funds, return
        if funds < amount + utils.calculate_fees(None):
            self.logger.warning("In sufficient funds, exiting, return")
            return

        # create transaction
        tx = CTransaction()

        # to the receiver
        txout = CTxOut()
        txout.nValue = amount
        txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(toaddress)
        tx.vout.append(txout)

        # from the sender
        nValueIn = 0
        nValueOut = amount
        public_keys = []
        private_keys = []
        # secrets = []
        for subaccount in subaccounts:
            # get received by from address
            previous_txouts = subaccount['received']
            for received in previous_txouts:
                txin = CTxIn()
                txin.prevout = COutPoint()
                txin.prevout.hash = received['txhash']
                txin.prevout.n = received['n']
                txin.scriptSig = received['scriptPubKey']
                tx.vin.append(txin)
                nValueIn = nValueIn + received['value']
                public_keys.append(subaccount['public_key'])
                private_keys.append(subaccount['private_key'])
                # secrets.append(subaccount['secret'])
                if nValueIn >= amount + utils.calculate_fees(tx):
                    break
            if nValueIn >= amount + utils.calculate_fees(tx):
                break

        # calculate the total excess amount
        excessAmount = nValueIn - nValueOut
        # calculate the fees
        fees = utils.calculate_fees(tx)
        # create change transaction, if there is any change left
        if excessAmount > fees:
            change_txout = CTxOut()
            change_txout.nValue = excessAmount - fees
            changeaddress = subaccounts[0]['address']
            change_txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(changeaddress)
            tx.vout.append(change_txout)

        # calculate txhash
        tx.calc_sha256()
        txhash = str(tx.sha256)
        # sign the transaction
        for public_key, private_key, txin in zip(public_keys, private_keys, tx.vin):
            key = CKey()
            key.set_pubkey(public_key)
            key.set_privkey(private_key)
            signature = key.sign(txhash)
            # scriptSig = chr(len(signature)) + hash_type + signature + chr(len(public_key)) + public_key
            scriptSig = chr(len(signature)) + signature + chr(len(public_key)) + public_key
            txin.scriptSig = scriptSig
        return tx


    # send to a vault
    def sendtovault(self, toaddress, tomaster_address, timeout, amount):
        # select the input addresses
        funds = 0
        subaccounts = []
        accounts = self.getaccounts()
        for account in accounts:
            for address, subaccount in account.iteritems():
                if subaccount['balance'] == 0:
                    continue
                else:
                    subaccounts.append(subaccount)
                    funds = funds + subaccount['balance']
                    if funds >= amount + utils.calculate_fees(None):
                        break

        # incase of insufficient funds, return
        if funds < amount + utils.calculate_fees(None):
            self.logger.warning("In sufficient funds, exiting, return")
            return

        # create transaction
        tx = CTransaction()

        # to the receiver
        txout = CTxOut()
        txout.nValue = amount
        vault_address = utils.addresses_to_vault_address(toaddress, tomaster_address, timeout)
        txout.scriptPubKey = utils.vault_address_to_pay_to_vault_script(vault_address)
        tx.vout.append(txout)

        # create vault
        self.newvault(vault_address, toaddress, tomaster_address, amount)

        # from the sender
        nValueIn = 0
        nValueOut = amount
        public_keys = []
        private_keys = []
        for subaccount in subaccounts:
            # get received by from address
            previous_txouts = subaccount['received']
            for received in previous_txouts:
                txin = CTxIn()
                txin.prevout = COutPoint()
                txin.prevout.hash = received['txhash']
                txin.prevout.n = received['n']
                txin.scriptSig = received['scriptPubKey']
                tx.vin.append(txin)
                nValueIn = nValueIn + received['value']
                public_keys.append(subaccount['public_key'])
                private_keys.append(subaccount['private_key'])
                if nValueIn >= amount + utils.calculate_fees(tx):
                    break
            if nValueIn >= amount + utils.calculate_fees(tx):
                break

        # calculate the total excess amount
        excessAmount = nValueIn - nValueOut
        # calculate the fees
        fees = utils.calculate_fees(tx)
        # create change transaction, if there is any change left
        if excessAmount > fees:
            change_txout = CTxOut()
            change_txout.nValue = excessAmount - fees
            changeaddress = self.getnewaddress()[1]
            change_txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(changeaddress)
            tx.vout.append(change_txout)

        # calculate txhash
        tx.calc_sha256()
        txhash = str(tx.sha256)
        self.logger.debug("Sending to vault %064x" % tx.sha256)
        # sign the transaction
        for public_key, private_key, txin in zip(public_keys, private_keys, tx.vin):
            key = CKey()
            key.set_pubkey(public_key)
            key.set_privkey(private_key)
            signature = key.sign(txhash)
            # scriptSig = chr(len(signature)) + hash_type + signature + chr(len(public_key)) + public_key
            scriptSig = chr(len(signature)) + signature + chr(len(public_key)) + public_key
            self.logger.debug("Adding signature: %s" % binascii.hexlify(scriptSig))
            txin.scriptSig = scriptSig
            self.logger.debug("Tx Validity: %064x" % tx.is_valid())
        # push data to vault
        tx.calc_sha256()
        self.set("vault:" + vault_address, {'txhash': tx.sha256})
        return (vault_address, tx)


    # withdraw from vault
    def withdrawfromvault(self, fromvaultaddress, toaddress, amount):
        vault = self.getvault(fromvaultaddress)
        received = self.chaindb.listreceivedbyvault(fromvaultaddress)
        received = received.values()[0]
        if received['value'] < amount + 2 * utils.calculate_fees(None):
            self.logger.warning("In sufficient funds in vault, exiting, return")
            return

        # create transaction
        tx = CTransaction()

        # to the receiver
        txout = CTxOut()
        txout.nValue = amount
        txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(toaddress)
        tx.vout.append(txout)

        # from the sender
        nValueIn = 0
        nValueOut = amount

        txin = CTxIn()
        txin.prevout = COutPoint()
        txin.prevout.hash = received['txhash']
        txin.prevout.n = received['n']
        txin.scriptSig = received['scriptPubKey']
        tx.vin.append(txin)

        # calculate nValueIn
        nValueIn = received['value']
        # calculate the total excess amount
        excessAmount = nValueIn - nValueOut
        # calculate the fees
        fees = 2 *                                                                                                                                                                 utils.calculate_fees(tx)
        # create change transaction, if there is any change left
        if excessAmount > fees:
            change_txout = CTxOut()
            change_txout.nValue = excessAmount - fees
            account = self.getaccount()
            changeaddress = fromvaultaddress
            self.logger.debug("Change address: %s" % changeaddress)
            change_txout.scriptPubKey = \
                utils.vault_address_to_pay_to_vault_script(changeaddress)
            tx.vout.append(change_txout)

        # calculate txhash
        tx.calc_sha256()
        txhash = str(tx.sha256)
        key = CKey()
        key.set_pubkey(vault['public_key'])
        key.set_privkey(vault['private_key'])
        signature = key.sign(txhash)
        # get the script
        timeout = 100
        script = utils.addresses_to_vault_script(vault['address'], \
            vault['master_address'], timeout)
        scriptSig = chr(OP_VAULT_WITHDRAW) + chr(len(signature)) + signature + script
        self.logger.debug("Adding signature: %s" % binascii.hexlify(scriptSig))
        txin.scriptSig = scriptSig
        return tx

    # TODO: enforce double use of vaults
    # TODO: remove amount
    def overridevaulttx(self, fromvaultaddress, toaddress, amount):
        vault = self.getvault(fromvaultaddress)
        # select the input addresses
        received = self.chaindb.listallreceivedbyvault(fromvaultaddress)
        received = received.values()[0]
        if received['value'] < 2 * utils.calculate_fees(None):
            self.logger.warning("In sufficient funds in vault, exiting, return")
            return
        # calculate remaining amount
        amount = received['value'] - 2 * utils.calculate_fees(None)
        # create transaction
        tx = CTransaction()

        # to the receiver
        txout = CTxOut()
        txout.nValue = amount
        txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(toaddress)
        tx.vout.append(txout)

        # from the sender
        nValueIn = 0
        nValueOut = amount

        txin = CTxIn()
        txin.prevout = COutPoint()
        txin.prevout.hash = received['txhash']
        txin.prevout.n = received['n']
        txin.scriptSig = received['scriptPubKey']
        tx.vin.append(txin)

        # calculate nValueIn
        nValueIn = received['value']
        # calculate the total excess amount
        excessAmount = nValueIn - nValueOut
        # calculate the fees
        fees = utils.calculate_fees(tx)
        # calculate txhash
        tx.calc_sha256()
        txhash = str(tx.sha256)
        key = CKey()
        key.set_pubkey(vault['public_key'])
        key.set_privkey(vault['private_key'])
        signature = key.sign(txhash)
        # get the script
        timeout = 100
        script = utils.addresses_to_vault_script(vault['address'], \
            vault['master_address'], timeout)
        scriptSig = chr(OP_VAULT_OVERRIDE) + chr(len(vault['master_public_key'])) + \
        vault['master_public_key'] + chr(len(signature)) + signature + script
        self.logger.debug("Adding signature: %s" % binascii.hexlify(scriptSig))
        txin.scriptSig = scriptSig
        return tx


    # fast withdraw from vault
    def fastwithdrawfromvault(self, fromvaultaddress, toaddress, amount):
        # select the input addresses
        funds = 0
        vault = self.getvault(fromvaultaddress)
        if vault['amount'] + utils.calculate_fees(None) < amount:
            self.logger.warning("In sufficient funds in vault, exiting, return")
            return

        # create transaction
        tx = CTransaction()

        # to the receiver
        txout = CTxOut()
        txout.nValue = amount
        txout.scriptPubKey = utils.address_to_pay_to_pubkey_hash(toaddress)
        tx.vout.append(txout)

        # from the sender
        nValueIn = 0
        nValueOut = amount

        txin = CTxIn()
        txin.prevout = COutPoint()
        received = self.chaindb.listreceivedbyvault(fromvaultaddress)
        # assuming vaults are not reused
        received = received.values()[0]
        txin.prevout.hash = received['txhash']
        txin.prevout.n = received['n']
        txin.scriptSig = received['scriptPubKey']
        tx.vin.append(txin)

        # calculate nValueIn
        nValueIn = received['value']
        # calculate the total excess amount
        excessAmount = nValueIn - nValueOut
        # calculate the fees
        fees = utils.calculate_fees(tx)
        # create change transaction, if there is any change left
        if excessAmount > fees:
            change_txout = CTxOut()
            change_txout.nValue = excessAmount - fees
            account = self.getaccount()
            changeaddress = fromvaultaddress
            self.logger.debug("Change address: %s" % changeaddress)
            change_txout.scriptPubKey = utils.vault_address_to_pay_to_vault_script(
                changeaddress)
            tx.vout.append(change_txout)

        # calculate txhash
        tx.calc_sha256()
        txhash = str(tx.sha256)
        mkey = CKey()
        mkey.set_pubkey(vault['master_public_key'])
        mkey.set_privkey(vault['master_private_key'])
        signature = mkey.sign(txhash)
        # get the script
        timeout = 100
        script = utils.addresses_to_vault_script(vault['address'], \
            vault['master_address'], timeout)
        scriptSig = chr(OP_VAULT_FAST_WITHDRAW)+chr(len(vault['master_public_key'])) \
        + vault['master_public_key'] + chr(len(signature)) + signature + script
        self.logger.debug("Adding signature: %s" % binascii.hexlify(scriptSig))
        txin.scriptSig = scriptSig
        return tx
