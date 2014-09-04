import os
import random
import threading
import time

class TimeVaultDaemon(threading.Thread):
     def run(self):
         os.system('timevaultd')

class VaultMiner(threading.Thread):
     def run(self):
         os.system('vaultminer')

def vaultsend(connection):
    account = connection.getaccount('account')

    # wait until you have generated some blocks
    while True:
        info = connection.getinfo()
        if info.blocks > 1:
            break
        time.sleep(1)

    # generate toaddresses
    toaddress = connection.getnewaddress()
    tomaster_address = connection.getnewaddress()
    timeout = random.randint(0, 50)
    amount = random.randint(0, 50)

    vaultaddress = connection.sendtovault(toaddress, tomaster_address,
        timeout, amount)
    return vaultaddress, amount


def waituntilvaultupdated(connection, vaultaddress):
    # check for updated balance
    while True:
        vaults = connection.getvaults()
        vault = vaults[vaultaddress]
        if vault['balance'] > 0:
            return vault
        time.sleep(1)

def waituntilvaultempty(connection, vaultaddress):
    # check for updated balance
    while True:
        vaults = connection.getvaults()
        vault = vaults[vaultaddress]
        if int(vault['balance']) == 0:
            return vault
        time.sleep(1)

def waituntilaccountupdated(connection, address):
    # check for updated balance
    while True:
        account = connection.getaccount('account')
        subaccount = account[address]
        if subaccount['balance'] > 0:
            return subaccount
        time.sleep(1)

def waituntilblocksgenerated(connection):
    # wait until you have generated some blocks
    while True:
        info = connection.getinfo()
        if info.blocks > 1:
            return info
        time.sleep(1)
