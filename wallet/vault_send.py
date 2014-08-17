from wallet import Wallet

wallet = Wallet()
account = wallet.getaccount()

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
wallet.sendtovault(toaddress, tomaster_address, timeout, amount)
