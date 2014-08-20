from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

print ('\nAccounts')
for subaccount in account.itervalues():
    print subaccount['address']  + ": ", subaccount['balance']

print ('\nVaults')
vaults = wallet.getvaults()
for vault in vaults:
    print vault['address']  + ": ", vault['balance']

print ('\nPending Transfers')
transactions = wallet.getpendingtransactions()
for transaction in transactions:
    print "From: ", transaction['fromaddress'], "To: ", transaction['toaddress'],\
        transaction['amount']
