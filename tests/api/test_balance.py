import sys
import random
import time
import unittest

from tests.api import base
from tests.api import utils
from timevault import bitcoinrpc

class TestBalance(base.TestBase):

    def test_big_vault_send(self):
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)
        amount = 500000000000
        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNotNone(vaultaddress)

        # wait for vault to get updated
        vault = utils.wait_until_vault_has_balance(self.connection, vaultaddress)
        self.assertEqual(int(vault['balance']), amount)

  
