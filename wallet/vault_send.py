import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser="user"
rpcpass="passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)

if len(account.itervalues()) < 2:
    print("Not enough accounts to create vault, quitting")
    sys.exit(1)

subaccount, vault_subaccount = account.itervalues()[:2]
toaddress = subaccount['address']
tomaster_address = vault_subaccount['address']
timeout = 20
amount = 20

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
connection.sendtovault(toaddress, tomaster_address, timeout, amount)
