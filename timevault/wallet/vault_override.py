from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

toaddress = wallet.getnewaddress()

print ('\nPending Transfers')
transactions = wallet.getpendingtransactions()
print transactions
for n, transaction in transactions.iteritems():
    print "\tId: ", n
    print "\tInputs: "
    for txin in transaction['inputs']:
        print "\t\t", txin
    print "\tOutputs: "
    for txout in transaction['outputs']:
        print "\t\t", txout

index = raw_input("Enter the id of the vault transaction you want to override: ")
fromaddress = transactions[index]['inputs'][0]
print "Fromaddress: ", fromaddress
amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
available_amount = 0
for output in transactions[index]['outputs']:
    available_amount = available_amount + int(output['amount'])
if available_amount < amount:
    print("In sufficient balance in vault, quitting")
    exit(1)

print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
wallet.overridevault(fromaddress, toaddress, amount)
