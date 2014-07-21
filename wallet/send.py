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
    if not subaccount['balance']:
        toaddress = subaccount['address']

if (not toaddress) and balance < 20:
    print("Not enough bitcoins in account, quitting")
    sys.exit(1)

amount = 20
print "Transferring: ", amount, " \tto: ", toaddress
connection.sendtoaddress(toaddress, amount)
