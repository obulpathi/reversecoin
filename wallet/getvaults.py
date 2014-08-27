from wallet import Wallet

wallet = Wallet()
vaults = wallet.getvaults()
for vault in vaults:
    print vault['address']  + ": ", vault['balance']
