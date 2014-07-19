import unittest

import utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.public_key_hex = '0432795c8e926a478bb664c2151e7ee341a5613fb6b48e6a56d5e8d24beec2edaa0169e8a12184b3e67ba43cb6d4acecc56e72eb5504d92a4aa770fdf8bdc6af85'
        self.private_key_hex = '3082011302010104209b40ca620768e361a681da9fd3b8b435cede7a810a0d138bd36de589c7a7be41a081a53081a2020101302c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010004010704410479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8022100fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a1440342000432795c8e926a478bb664c2151e7ee341a5613fb6b48e6a56d5e8d24beec2edaa0169e8a12184b3e67ba43cb6d4acecc56e72eb5504d92a4aa770fdf8bdc6af85'
        self.address = '1AomE4FUvr9AdsuVupsVU2V149esiE6k8d'

    def test_public_key_hex_to_address(self):
        address = utils.public_key_to_address(self.public_key_hex)

        # should raise an exception for an immutable sequence
        self.assertEqual(self.address, address)

if __name__ == '__main__':
    unittest.main()
