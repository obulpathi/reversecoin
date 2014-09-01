import os
import sys
import random
import time
import threading
import unittest

from base import TestBase
from timevault import bitcoinrpc

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

class TestWallet(TestBase):
    @classmethod
    def setUpClass(cls):
        vaultd = TimeVaultDaemon()
        miner = VaultMiner()
        vaultd.start()
        miner.start()
        time.sleep(2)


    def setUp(self):
        rpcuser = "user"
        rpcpass = "passwd"
        self.account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)


    def test_account(self):
        account = self.connection.getaccount(self.account)
        self.assertIsInstance(account, dict)
        for subaccount in account.itervalues():
            self.assertIn('address', subaccount)
            self.assertIn('public_key', subaccount)
            self.assertIn('private_key', subaccount)
            self.assertIn('balance', subaccount)


    def test_info(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)


    def test_newaddress(self):
        address = self.connection.getnewaddress()
        self.assertIsNotNone(address)


    def test_send(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        # generate a new toaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, 50)
        self.connection.sendtoaddress(toaddress, amount)

        account = self.connection.getaccount(self.account)
        self.assertIn(toaddress, account)

        # wait for account to get updated
        subaccount = waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def test_vault_send(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)


    def test_vault_withdraw(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def test_vault_override(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait until withdraw begins
        vault = waituntilvaultempty(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), 0)

        # initiate vault override
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.vaultoverride(fromaddress, toaddress, amount)

        # check for updated balance
        subaccount = waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def test_vault_fast_withdraw(self):
        # wait until blocks are generated
        info = waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate fast withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass
