from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

balance = 0
for subaccount in account.itervalues():
    balance = balance + subaccount['balance']

amount = int(input("Enter the balance to transfer to vault: "))

if balance < amount:
    print("Not enough balance")
    exit(1)

toaddress = wallet.getnewaddress()
tomaster_address = wallet.getnewaddress()
timeout = 20
maxfees = 10

print("Transfering: %d toaddress: %s tomaster_address: %s" % \
     (amount, toaddress, tomaster_address))
wallet.sendtovault(toaddress, tomaster_address, amount, timeout, maxfees)
