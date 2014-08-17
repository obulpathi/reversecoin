import sys
from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

# create vault
if len(account) < 2:
    print("Not enough accounts to create vault, quitting")
    sys.exit(1)

balance = 0
for subaccount in account.itervalues():
    balance = balance + subaccount['balance']

if balance < 20:
    print("Not enough balance")
    exit(2)

subaccount, vault_subaccount = list(account.itervalues())[:2]
toaddress = subaccount['address']
tomaster_address = vault_subaccount['address']
timeout = 20
amount = 20

print("Transfering: %d toaddress: %s tomaster_address: %s" % \
     (amount, toaddress, tomaster_address))
connection.sendtovault(toaddress, tomaster_address, timeout, amount)





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

if not fromaddress:
    print("No vault account, quitting")
    sys.exit(1)
if not toaddress:
    print("No empty accounts, quitting")
    sys.exit(1)

amount = 15
print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
connection.withdrawfromvault(fromaddress, toaddress, amount)
