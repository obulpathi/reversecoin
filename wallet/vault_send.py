import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser="user"
rpcpass="passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)

if len(account) < 2:
    print("Not enough accounts to create vault, quitting")
    sys.exit(1)

subaccount, vault_subaccount = list(account.itervalues())[:2]
toaddress = subaccount['address']
tomaster_address = vault_subaccount['address']
timeout = 20
amount = 20

print("Transfering: " + str(amount) + "\ttoaddress: " + toaddress + "\ttomaster_address: " + tomaster_address)
connection.sendtovault(toaddress, tomaster_address, timeout, amount)
