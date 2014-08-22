from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

toaddress = None
for subaccount in account.itervalues():
    if not toaddress:
        toaddress = subaccount['address']
        break
else:
    print("No enough addresses to send to, quitting")
    exit(1)

print ('\nPending Transfers')
transactions = wallet.getpendingtransactions()
for n, transaction in enumerate(transactions):
    print "Id: ", n, "From: ", transaction['fromaddress'], "To: ", \
        transaction['toaddress'], transaction['amount']

index = int(input("Enter the id of the vault transaction you want to override: "))
fromaddress = transactions[index]['fromaddress']
amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
if transactions[index]['amount'] < amount + 2:
    print("In sufficient balance in vault, quitting")
    exit(2)

print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
wallet.fastwithdrawfromvault(fromaddress, toaddress, amount)
