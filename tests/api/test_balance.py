import sys
import random
import time
import unittest

from tests.api import base
from tests.api import utils
from timevault import bitcoinrpc

class TestBalance(base.TestBase):

    def test_send_more_than_balance(self):
        pass
