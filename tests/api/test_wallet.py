import sys
import random
import time
import unittest

from tests.api import base
from tests.api import utils
from timevault import bitcoinrpc

class TestWallet(base.TestBase):
    @classmethod
    def setUpClass(cls):
        vaultd = utils.TimeVaultDaemon()
        miner = utils.VaultMiner()
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
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)


    def test_newaddress(self):
        address = self.connection.getnewaddress()
        self.assertIsNotNone(address)


    def test_send(self):
        # wait until blocks are generated
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        # generate a new toaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, 50)
        self.connection.sendtoaddress(toaddress, amount)

        account = self.connection.getaccount(self.account)
        self.assertIn(toaddress, account)

        # wait for account to get updated
        subaccount = utils.waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def test_vault_send(self):
        # wait until blocks are generated
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = utils.vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

    def test_vault_withdraw(self):
        # wait until blocks are generated
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = utils.vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = utils.waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def test_vault_override(self):
        # wait until blocks are generated
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, vaultamount = utils.vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), vaultamount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, vaultamount-1)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait until withdraw begins
        vault = utils.waituntilvaultempty(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), 0)

        # initiate vault override
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = vaultamount - 2
        self.connection.overridevaulttx(fromaddress, toaddress, amount)

        # check for updated balance
        subaccount = utils.waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)

    def test_vault_fast_withdraw(self):
        # wait until blocks are generated
        info = utils.waituntilblocksgenerated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultaddress, amount = utils.vaultsend(self.connection)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.waituntilvaultupdated(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate fast withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(0, amount)
        self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = utils.waituntilaccountupdated(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        pass
