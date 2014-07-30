import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser = "user"
rpcpass = "passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)

fromaddress = None
toaddress = None
for subaccount in account.itervalues():
    if not fromaddress and subaccount['address'][0] == '4' \
        and subaccount['balance'] > 20:
        fromaddress = subaccount['address']
    elif not toaddress and subaccount['address'][0] == '1':
        toaddress = subaccount['address']
    if fromaddress and toaddress:
        break

if not fromaddress:
    print("No vault accounts to send from, quitting")
    sys.exit(1)

if not toaddress):
    print("No empty accounts to send, quitting")
    sys.exit(1)

amount = 15
print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
connection.fastwithdrawfromvault(fromaddress, toaddress, amount)
