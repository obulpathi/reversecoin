import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser="user"
rpcpass="passwd"

print sys.argv
fromaddress = sys.argv[1]
toaddress = sys.argv[2]
amount = int(sys.argv[4])

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
connection.override_vault(fromaddress, toaddress, amount)
