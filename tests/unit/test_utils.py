import unittest

from timevault.bitcoin import utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_public_key_to_address(self):
        public_key, private_key, address = utils.getnewaddress()
        myaddress = utils.public_key_to_address(public_key)
        self.assertEqual(address, myaddress)

if __name__ == '__main__':
    unittest.main()

"""
def test_create_vault_address(pubkey_hex):
    vault_address = utils.public_key_to_vault_address(pubkey_hex)
    print(vault_address)

def test_create_vault_script(address, master_address, timeout, fees):
    vault_script = utils.addresses_to_vault_script(address, master_address, timeout, fees)
    print(binascii.hexlify(vault_script))

def test_addresses_to_vault_address(address, master_address, timeout):
    vault_address = utils.addresses_to_vault_address(address, master_address, timeout)
    print(vault_address)
"""
