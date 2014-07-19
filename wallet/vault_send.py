import sys
import bitcoinrpc
from bitcoinrpc.exceptions import InsufficientFunds

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser="user"
rpcpass="passwd"

print sys.argv
toaddress = sys.argv[1]
tomaster_address = sys.argv[2]
timeout = int(sys.argv[3])
amount = int(sys.argv[4])

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
connection.sendtovault(toaddress, tomaster_address, timeout, amount)
