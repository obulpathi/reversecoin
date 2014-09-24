import os
import sys
import subprocess
import random
import time
import unittest

from tests.api import base
from tests.api import utils
from timevault import bitcoinrpc

class TestWallet(base.TestBase):
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
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

    def test_newaddress(self):
        address = self.connection.getnewaddress()
        self.assertIsNotNone(address)

    def test_send(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        # generate a new toaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(20, 30)
        self.connection.sendtoaddress(toaddress, amount)

        account = self.connection.getaccount(self.account)
        self.assertIn(toaddress, account)

        # wait for account to get updated
        subaccount = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)

    def test_vault_send(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

    def test_vault_withdraw(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(1, amount-2)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)

    def test_vault_withdraw_more_than_balance(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        transfered = self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # assert that no balance has been transfered
        self.assertEqual(0, transfered)

        # wait until few more blocks are generated
        utils.wait_until_n_blocks_are_generated(self.connection, 2)

        # assert that the balances are still the same
        vaults = self.connection.getvaults()
        vault = vaults[vaultaddress]
        self.assertEqual(int(vault['balance']), amount)

    def test_multiple_vault_withdraws(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        withdrawamount = random.randint(1, amount/2)
        self.connection.withdrawfromvault(fromaddress, toaddress, withdrawamount)

        # wait for account to get updated
        subaccount = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), withdrawamount)
        time.sleep(10)
        vault = self.connection.getvaults()[vaultaddress]
        self.assertEqual(int(vault['balance']), amount - withdrawamount - 2)

        amount = int(vault['balance'])
        # initiate another vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        withdrawamount = random.randint(1, amount-2)
        self.connection.withdrawfromvault(fromaddress, toaddress, withdrawamount)

        # wait for account to get updated
        subaccount = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), withdrawamount)
        vault = self.connection.getvaults()[vaultaddress]
        self.assertEqual(int(vault['balance']), amount - withdrawamount - 2)

    def test_vault_override(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        vaultamount = 45
        vaultaddress = utils.send_to_vault(self.connection, vaultamount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), vaultamount)

        # initiate vault withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(1, vaultamount-2)
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

        # wait until withdraw begins
        vault = utils.wait_until_vault_is_empty(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), 0)

        # initiate vault override
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = vaultamount - 2
        self.connection.overridevaulttx(fromaddress, toaddress, amount)

        # check for updated balance
        account = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(account['balance']), amount)

    def test_vault_fast_withdraw(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

        # initiate fast withdraw
        fromaddress = vaultaddress
        toaddress = self.connection.getnewaddress()
        amount = random.randint(1, amount-1)
        self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)

        # wait for account to get updated
        subaccount = utils.wait_until_account_has_balance(self.connection, toaddress)
        self.assertEqual(int(subaccount['balance']), amount)

    def test_vault_uniqueness(self):
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        amount = 45
        timeout = 10
        maxfees = 10
        toaddress = self.connection.getnewaddress()
        tomaster_address = self.connection.getnewaddress()

        vaultaddress = self.connection.sendtovault(toaddress, tomaster_address,
            amount, timeout, maxfees)
        self.assertIsNotNone(vaultaddress)

        # try recreating vault
        vaultaddress = self.connection.sendtovault(toaddress, tomaster_address,
            amount, timeout, maxfees)
        self.assertIsNone(vaultaddress)
