import sys
import random
import time
import unittest

from tests.api import base
from tests.api import utils
from reversecoin import bitcoinrpc

class TestBalance(base.TestBase):

    def test_spend_more_than_balance(self):
        LARGE_AMOUNT = 500000000000

        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        total_balance = utils.get_total_balance(self.connection)
        amount = total_balance + LARGE_AMOUNT

        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNone(vaultaddress)

    def test_vault_send_more_than_balance(self):
        LARGE_AMOUNT = 500000000000
        # wait until blocks are generated
        info = utils.wait_until_blocks_are_generated(self.connection)
        self.assertTrue(info.blocks >= -1)

        total_balance = utils.get_total_balance(self.connection)
        amount = total_balance + LARGE_AMOUNT

        vaultaddress = utils.send_to_vault(self.connection, amount)
        self.assertIsNone(vaultaddress)
