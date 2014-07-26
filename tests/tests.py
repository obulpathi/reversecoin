import utils
from bitcoin.key import CKey


def test_create_vault_address(pubkey_hex):
    vault_address = utils.public_key_to_vault_address(pubkey_hex)
    print(vault_address)

def test_create_vault_script(address, master_address, timeout, fees):
    vault_script = utils.addresses_to_vault_script(address, master_address, timeout, fees)
    print(binascii.hexlify(vault_script))

def test_addresses_to_vault_address(address, master_address, timeout):
    vault_address = utils.addresses_to_vault_address(address, master_address, timeout)
    print(vault_address)

if __name__ == "__main__":
    address = "17zrFecjrd5nbv3oFDNKtX5wb1QxvaDdjE"
    master_address = "1GbMmidTU3gGjz6S85B4JPv33B12VE8S3U"
    timeout = 100
    test_addresses_to_vault_address(address, master_address, timeout)
