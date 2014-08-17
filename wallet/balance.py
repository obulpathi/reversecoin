from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

for subaccount in account.itervalues():
    print subaccount['address']  + ": ", subaccount['balance']
