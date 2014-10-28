import sys
import argparse

from timevault.wallet.wallet import Wallet
from timevault import bitcoinrpc
from timevault.version import VERSION, COPYRIGHT_YEAR

def address():
    wallet = Wallet()
    address = wallet.getnewaddress()
    print address

def account():
    wallet = Wallet()
    account = wallet.getaccount()

    for subaccount in account.itervalues():
        print "Address: ", subaccount['address']
        print "Public key: ", subaccount['public_key']
        print "Private key: ", subaccount['private_key']
        print "Balance: ", subaccount['balance']
        print "\n\n"

def balance():
    wallet = Wallet()
    account = wallet.getaccount()

    print ('\nAccounts')
    for subaccount in account.itervalues():
        print subaccount['address']  + ": ", subaccount['balance']

    print ('\nVaults')
    vaults = wallet.getvaults()
    for vault in vaults.itervalues():
        print vault['address']  + ": ", vault['balance']

    print ('\nPending Transfers')
    transactions = wallet.getpendingtransactions()
    for transaction in transactions.itervalues():
        fromaddress = transaction['inputs'][0]
        for txouts in transaction['outputs']:
            print fromaddress, "->", txouts['toaddress'] + ": ", txouts['amount']

def getvaults():
    wallet = Wallet()
    vaults = wallet.getvaults()
    for vault in vaults:
        print vault['address']  + ": ", vault['balance']

def blockchain():
    wallet = Wallet()
    wallet.dumpblockchain()

def mempool():
    wallet = Wallet()
    wallet.dumpmempool()

def received():
    # JSON-RPC server user, password.  Uses HTTP Basic authentication.
    rpcuser="user"
    rpcpass="passwd"

    address = input("Enter the address to check received transactions:")

    connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
    txoutlist = connection.getreceivedbyaddress(address)

    for txout in txoutlist:
        print txout

def send():
    wallet = Wallet()
    account = wallet.getaccount()

    toaddress = wallet.getnewaddress()
    balance = 0
    for subaccount in account.itervalues():
        balance = balance + subaccount['balance']

    amount = int(input("Enter the balance to transfer to address: "))

    if balance < amount:
        print("Not enough balance")
        exit(1)

    print "Transferring: ", amount, " \tto: ", toaddress
    wallet.connection.sendtoaddress(toaddress, amount)

def getvault():
    # JSON-RPC server user, password.  Uses HTTP Basic authentication.
    rpcuser = "user"
    rpcpass = "passwd"

    print("Not implemented yet!")
    exit(1)

    connection = bitcoinrpc.connect_to_remote(
        rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
    vaults = connection.getvaults()
    for vault in vaults.itervalues():
        print("Name: %s" % vault['name'])
        print("Address: %s" % vault['address'])
        print("Master Address: %s" % vault['master_address'])
        print("Balance: %d" % vault['amount'])
        """
        #print "Public key: ", vault['public_key']
        #print "Private key: ", vault['private_key']
        #print "Master Public key: ", vault['master_public_key']
        #print "Master Private key: ", vault['master_private_key']
        """
        print "\n\n"

def savings():
    # JSON-RPC server user, password.  Uses HTTP Basic authentication.
    rpcuser = "user"
    rpcpass = "passwd"
    account = "account"

    connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
    account = connection.getaccount(account)
    for subaccount in account.itervalues():
        print subaccount['address']  + ": ", subaccount['balance']

def vault_send():
    wallet = Wallet()
    account = wallet.getaccount()

    balance = 0
    for subaccount in account.itervalues():
        balance = balance + subaccount['balance']

    amount = int(input("Enter the balance to transfer to vault: "))

    if balance < amount:
        print("Not enough balance")
        exit(1)

    toaddress = wallet.getnewaddress()
    tomaster_address = wallet.getnewaddress()
    timeout = 20
    maxfees = 10

    print("Transfering: %d toaddress: %s tomaster_address: %s" % \
          (amount, toaddress, tomaster_address))
    wallet.sendtovault(toaddress, tomaster_address, amount, timeout, maxfees)

def vault_withdraw():
    wallet = Wallet()
    account = wallet.getaccount()
    toaddress = wallet.getnewaddress()

    print("Available vaults")
    vaults = wallet.getvaults()
    for n, vault in enumerate(vaults.itervalues()):
        print "Id: ", n, vault['address']  + ": ", vault['balance']
    index = int(input("Enter the id of the vault you want to transfer balance from: "))

    for n, vault in enumerate(vaults.itervalues()):
        if index == n:
            fromaddress = vault['address']

    amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
    if vaults[fromaddress]['balance'] < amount + 2:
        print("In sufficient balance in vault, quitting")
        exit(2)

    print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
    wallet.withdrawfromvault(fromaddress, toaddress, amount)

def vault_override():
    wallet = Wallet()
    account = wallet.getaccount()
    toaddress = wallet.getnewaddress()

    print ('\nPending Transfers')
    transactions = wallet.getpendingtransactions()

    for n, transaction in transactions.iteritems():
        print "\tId: ", n
        print "\t\tInput:", transaction['inputs'][0]
        print "\t\tOutputs: "
        for txout in transaction['outputs']:
            print "\t\t\t", txout['amount'], "->", txout['toaddress']

    index = raw_input("Enter the id of the vault transaction you want to override: ")
    fromaddress = transactions[index]['inputs'][0]
    print "Fromaddress: ", fromaddress
    print "Toaddress: ", toaddress
    print("Overriding the transaction")
    wallet.overridevault(fromaddress, toaddress)

def vault_fast_withdraw():
    wallet = Wallet()
    toaddress = wallet.getnewaddress()

    print("Available vaults")
    vaults = wallet.getvaults()
    vaults = list(vaults.itervalues())
    for n, vault in enumerate(vaults):
        print "Id: ", n, vault['address']  + ": ", vault['balance']
    index = int(input("Enter the id of the vault you want to transfer balance from: "))
    fromaddress = vaults[index]['address']
    amount = int(input("Enter the balance to transfer from: {}: ".format(fromaddress)))
    if vaults[index]['balance'] < amount + 2:
        print("In sufficient balance in vault, quitting")
        exit(2)

    print("Transfering: " + str(amount) + "\tfrom address: " + fromaddress + "\tto address: " + toaddress)
    wallet.fastwithdrawfromvault(fromaddress, toaddress, amount)

def vault_pending():
    wallet = Wallet()
    account = wallet.getaccount()

    print ('\nPending Transfers')
    transactions = wallet.getpendingtransactions()

    for n, transaction in transactions.iteritems():
        print "\tId: ", n
        print "\t\tInput:", transaction['inputs'][0]
        print "\t\tOutputs: "
        for txout in transaction['outputs']:
            print "\t\t\t", txout['amount'], "->", txout['toaddress']


def run(args):
    globals()[args.command]()

# any function added above should be registered here
_SUPPORTED_COMMANDS = [
    ("address", "Generate a new address.",),
    ("account", "Look at the account summary.",),
    ("balance", "Current wallet balance.",),
    ("getvaults", "Highlevel information about the vaults.",),
    ("blockchain", "Dump the current block chain.",),
    ("mempool", "Dump the mempool.",),
    ("received", "Received transactions.",),
    ("send", "Send coins.",),
    ("getvault", "A little detailed view of vaults.",),
    ("savings", "Balance in each account.",),
    ("vault_send", "Send to a vault.",),
    ("vault_withdraw", "Withdraw from a vault.",),
    ("vault_override", "Override a vault transaction.",),
    ("vault_fast_withdraw", "Withdraw from a vault immediately. No timeout associated.",),
    ("vault_pending", "List of pending vault transactions.",),
    ]

_EPILOG = "Commands Desription:\n====================\n"
for cmd, hlp in _SUPPORTED_COMMANDS:
    _EPILOG += "{:<30} {}\n".format(cmd, hlp)

_WALLET_NAME = """
Timevault Wallet - v%s

Copyright: %s
""" % (VERSION, COPYRIGHT_YEAR)

def parse_arguments():

    parser = argparse.ArgumentParser(description=_WALLET_NAME,
                                     epilog=_EPILOG,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=[c for c,_ in _SUPPORTED_COMMANDS])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

def main():
    args = parse_arguments()
    run(args)

if __name__ == "__main__":
    main()
