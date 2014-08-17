import unittest

import bitcoinrpc


class TestWallet(unittest.TestCase):

    def setUp(self):
        rpcuser = "user"
        rpcpass = "passwd"
        account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)

    def test_info(self):
        pass

    def test_balance(self):
        pass

    def test_account(self):
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
        pass

if __name__ == '__main__':
    unittest.main()
