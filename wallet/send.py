import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser="user"
rpcpass="passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)

toaddress = ''
balance = 0
for subaccount in account.itervalues():
    balance = balance + subaccount['balance']
    if subaccount['balance'] == 0:
        toaddress = subaccount['address']

if not toaddress:
    print("No account with zero balance, quitting")
    sys.exit(1)

if balance < 20:
    print("Not enough bitcoins in account, quitting")
    sys.exit(1)

amount = 20
print "Transferring: ", amount, " \tto: ", toaddress
connection.sendtoaddress(toaddress, amount)
