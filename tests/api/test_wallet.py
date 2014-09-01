import os
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

        self.assertTrue(info.blocks >= 1)


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
        account = self.connection.getaccount(self.account)

        # wait until you have generated some blocks
        while True:
            info = self.connection.getinfo()
            if info.blocks > 1:
                break
            time.sleep(1)

        # generate toaddresses
        toaddress = self.connection.getnewaddress()
        tomaster_address = self.connection.getnewaddress()
        timeout = random.randint(0, 50)
        amount = random.randint(0, 50)

        vault_address = self.connection.sendtovault(toaddress, tomaster_address,
            timeout, amount)
        self.assertIsNotNone(vault_address)

        test_vault = None
        flag = False
        while not flag:
            vaults = self.connection.getvaults()
            for vault in vaults:
                if vault['address'] == vault_address and vault['balance'] > 0:
                    test_vault = vault
                    flag = True
            time.sleep(1)

        # check if the new balance is reflected
        self.assertEqual(int(test_vault['balance']), amount)


    @unittest.skip("Not Implemented")
    def test_vault_withdraw(self):
        pass


    @unittest.skip("Not Implemented")
    def test_vault_fast_withdraw(self):
        account = self.connection.getaccount(self.account)

        # wait until you have generated some blocks
        while True:
            info = self.connection.getinfo()
            if info.blocks > 1:
                break
            time.sleep(1)

        # generate toaddresses
        toaddress = self.connection.getnewaddress()
        tomaster_address = self.connection.getnewaddress()
        timeout = random.randint(0, 50)
        amount = random.randint(0, 50)

        self.connection.sendtovault(toaddress, tomaster_address, timeout, amount)

        vaults = wallet.getvaults()
        for n, vault in enumerate(vaults):
            print "Id: ", n, vault['address']  + ": ", vault['balance']
        index = int(input("Enter the id of the vault you want to transfer balance from: "))
        fromaddress = vaults[index]['address']
        amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
        if vaults[index]['balance'] < amount + 2:
            print("In sufficient balance in vault, quitting")
            exit(2)

        print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
        wallet.fastwithdrawfromvault(fromaddress, toaddress, amount)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass
