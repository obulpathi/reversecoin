from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

balance = 0
for subaccount in account.itervalues():
    balance = balance + subaccount['balance']

if balance < 20:
    print("Not enough balance")
    exit(1)

toaddress = wallet.getnewaddress()
tomaster_address = wallet.getnewaddress()
timeout = 20
amount = 20

print("Transfering: %d toaddress: %s tomaster_address: %s" % \
     (amount, toaddress, tomaster_address))
wallet.sendtovault(toaddress, tomaster_address, timeout, amount)
