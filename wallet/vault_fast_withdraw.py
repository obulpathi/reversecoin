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

print("Available vaults")
vaults = wallet.getvaults()
for n, vault in enumerate(vaults):
    print "Id: ", n, vault['address']  + ": ", vault['balance']
index = int(input("Enter the id of the vault you want to transfer balance from: "))
fromaddress = vaults[index]['address']
amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
if vaults[index]['balance'] < amount + 2:
    print("In sufficient balance in vault, quitting")
    exit(2)

print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
wallet.fastwithdrawfromvault(fromaddress, toaddress, amount)
