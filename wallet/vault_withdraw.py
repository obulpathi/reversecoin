import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser = "user"
rpcpass = "passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)

fromaddress = ''
toaddress = ''
for subaccount in account.itervalues():
    if subaccount['address'][0] == '4':
        fromaddress = subaccount['address']
    if not toaddress and subaccount['address'][0] == '1':
        toaddress = subaccount['address']
    if fromaddress and toaddress:
        break

if not (fromaddress and toaddress):
    print("Not enough accounts, quitting")
    sys.exit(1)

amount = 15

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
connection.withdrawfromvault(fromaddress, toaddress, amount)
