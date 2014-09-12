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

def send_to_vault(connection, amount, timeout = None, maxfees = None):
    if not timeout:
        timeout = 10
    if not maxfees:
        maxfees = 10

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

    vaultaddress = connection.sendtovault(toaddress, tomaster_address,
        amount, timeout, maxfees)
    return vaultaddress


def wait_until_vault_has_balance(connection, vaultaddress):
    # check for updated balance
    while True:
        vaults = connection.getvaults()
        vault = vaults[vaultaddress]
        if vault['balance'] > 0:
            return vault
        time.sleep(1)

def wait_until_vault_is_empty(connection, vaultaddress):
    # check for updated balance
    while True:
        vaults = connection.getvaults()
        vault = vaults[vaultaddress]
        if int(vault['balance']) == 0:
            return vault
        time.sleep(1)

def wait_until_account_has_balance(connection, address):
    # check for updated balance
    while True:
        account = connection.getaccount('account')
        subaccount = account[address]
        if subaccount['balance'] > 0:
            return subaccount
        time.sleep(1)

def wait_until_blocks_are_generated(connection):
    # wait until you have generated some blocks
    while True:
        info = connection.getinfo()
        if info.blocks > 1:
            return info
        time.sleep(1)
