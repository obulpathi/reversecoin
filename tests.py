import utils
from bitcoin.key import CKey


def test_create_vault_address(pubkey_hex):
    vault_address = utils.public_key_to_vault_address(pubkey_hex)
    print vault_address

def test_create_vault_script(address, master_address, timeout, fees):
    vault_script = utils.addresses_to_vault_script(address, master_address, timeout, fees)
    print binascii.hexlify(vault_script)

if __name__ == "__main__":
    key = CKey()
    key.generate()
    private_key = key.get_privkey()
    public_key = key.get_pubkey()
    test_create_vault_address(public_key)
