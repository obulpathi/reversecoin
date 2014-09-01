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

def vault_send(connection):
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
        info = self.connection.getinfo()

        self.assertTrue(info.blocks >= -1)


    def test_newaddress(self):
        address = self.connection.getnewaddress()

        self.assertIsNotNone(address)


    @unittest.skip("Need to fix the walletdb")
    def test_send(self):
        account = self.connection.getaccount(self.account)

        # wait until you have generated some blocks
        while True:
            info = self.connection.getinfo()
            if info.blocks > 1:
                break
            time.sleep(1)

        # generate a new toaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, 50)
        self.connection.sendtoaddress(toaddress, amount)

        account = self.connection.getaccount(self.account)
        self.assertIn(toaddress, account)

        while True:
            account = self.connection.getaccount(self.account)
            if account[toaddress]['balance'] > 0:
                break
            time.sleep(1)

        # check if the new balance is reflected
        self.assertEqual(account[toaddress]['balance'], amount)


    def test_vault_send(self):
        vaultaddress, amount = vault_send(self.connection)
        self.assertIsNotNone(vaultaddress)

        # check for updated balance
        while True:
            vaults = self.connection.getvaults()
            vault = vaults[vaultaddress]
            if vault['balance'] > 0:
                self.assertEqual(int(vault['balance']), amount)
                break
            time.sleep(1)


    @unittest.skip("Not Implemented")
    def test_vault_withdraw(self):
        pass


    def test_vault_fast_withdraw(self):
        vaultaddress, amount = vault_send(self.connection)
        self.assertIsNotNone(vaultaddress)

        # check for updated balance
        while True:
            vaults = self.connection.getvaults()
            vault = vaults[vaultaddress]
            if vault['balance'] > 0:
                self.assertEqual(int(vault['balance']), amount)
                break
            time.sleep(1)

        # initiate fast withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)

        # check for updates balance
        while True:
            account = self.connection.getaccount(self.account)
            subaccount = account[toaddress]
            if subaccount['balance'] > 0:
                self.assertEqual(int(subaccount['balance']), amount)
                break
            time.sleep(1)

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass
