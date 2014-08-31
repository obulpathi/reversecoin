import unittest

from base import TestBase
from timevault import bitcoinrpc

class TestWallet(TestBase):
    def setUp(self):
        super(TestBase, self).setUp()
        rpcuser = "user"
        rpcpass = "passwd"
        account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)

    def test_account(self):
        account = self.connection.getaccount("account")
        self.assertIsInstance(account, dict)
        for subaccount in account.itervalues():
            self.assertIn('address', subaccount)
            self.assertIn('public_key', subaccount)
            self.assertIn('private_key', subaccount)
            self.assertIn('balance', subaccount)

    """
    # FIXME
    def test_info(self):
        pass

    def test_balance(self):
        pass

    def test_send(self):
        pass

    def test_vault_send(self):
        pass

    def test_vault_withdraw(self):
        pass

    def test_vault_fast_withdraw(self):
        pass

    def testDown(self):
        super(TestBase, self).tearDown()
    """
