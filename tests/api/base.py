import unittest

from timevault import bitcoinrpc


class TestBase(unittest.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        rpcuser = "user"
        rpcpass = "passwd"
        account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)

    def tearDown(self):
        pass
