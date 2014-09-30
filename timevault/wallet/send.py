from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

toaddress = wallet.getnewaddress()
balance = 0
for subaccount in account.itervalues():
    balance = balance + subaccount['balance']

amount = int(input("Enter the balance to transfer to address: "))

if balance < amount:
    print("Not enough balance")
    exit(1)

print "Transferring: ", amount, " \tto: ", toaddress
wallet.connection.sendtoaddress(toaddress, amount)
