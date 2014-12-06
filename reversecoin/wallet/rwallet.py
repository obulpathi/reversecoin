import sys
import argparse

from reversecoin.wallet.wallet import Wallet
from reversecoin import bitcoinrpc
from reversecoin.bitcoinrpc.exceptions import TransportException
from reversecoin.version import VERSION, COPYRIGHT_YEAR


def getindex(msg, min_index=0, max_index=None):
    try:
        index = int(raw_input("{0}: ".format(msg)))
    except Exception as e:
        print("Please enter a valid id.")
        exit(1)
    if index < min_index:
        print("Please enter a valid id.")
        exit(2)
    if (max_index is not None) and (index > max_index):
        print("Please enter a valid id.")
        exit(3)
    return index

def getamount(msg, min_amount = 1, max_amount = None):
    try:
        amount = int(input("{0}: ".format(msg)))
    except Exception as e:
        print("Please enter a valid amount.")
        exit(1)
    if amount < min_amount:
        print("Please enter a valid amount.")
        exit(2)
    if (max_amount is not None) and amount > max_amount:
        print("Please enter a valid amount.")
        exit(3)
    return amount

def getaddress(msg, wallet):
    account = wallet.getaccount()
    if not account:
        print("No accounts created yet!")
        exit(1)
    addresses = [address for address in account]
    for count, address in enumerate(addresses):
        print("Id: {0}\t{1}".format(count+1, address))
    index = getindex(msg, 1, len(addresses))
    return addresses[index-1]

def getemptyvault(msg, wallet):
    vaults = wallet.getvaults()
    emptyvaults = [vault for vault in vaults if not vault['balance']]
    if not emptyvaults:
        print("No empty vaults, please create one!")
        exit(1)

    for count, vault in enumerate(emptyvaults):
        print("{0}: {1}".format(count, vault))

    index = getindex(msg, min_index=0, max_index=len(emptyvaults)-1)
    return emptyvaults[index]

def info(wallet):
    info = wallet.getinfo()
    print("Blocks: {0}".format(info.blocks))

def newaddress(wallet):
    address = wallet.getnewaddress()
    print address

def account(wallet):
    account = wallet.getaccount()
    if not account:
        print("No accounts created yet!")
    for subaccount in account.itervalues():
        print("Address: {0}".format(subaccount['address']))
        print("Public key: {0}".format(subaccount['public_key']))
        print("Private key: {0}".format(subaccount['private_key']))
        print("Balance: {0}".format(subaccount['balance']))
        print("\n\n")

def balance(wallet):
    account = wallet.getaccount()
    print("\nAccounts")
    if not account:
        print("\tNo accounts created yet!")
    for subaccount in account.itervalues():
        print subaccount['address']  + ": ", subaccount['balance']

    print("\nVaults")
    vaults = wallet.getvaults()
    if not vaults:
        print("\tNo vaults created yet!")
    for vault in vaults.itervalues():
        print vault["name"]  + ": ", vault["balance"]

    transactions = wallet.getpendingtransactions()
    print("\nPending Transfers")
    if not transactions:
        print("\tNo pending transactions!")
    for transaction in transactions.itervalues():
        fromaddress = transaction["inputs"][0]
        for txouts in transaction["outputs"]:
            print fromaddress, "->", txouts["toaddress"] + ": ", txouts["amount"]

def blockchain(wallet):
    wallet.dumpblockchain()

def mempool(wallet):
    wallet.dumpmempool()

def received(wallet):
    msg = "Enter the id of the address to check received transactions"
    address = getaddress(msg, wallet)
    txouts = wallet.received(address)
    if not txouts:
        print("This address did not receive any transactions!")
        exit(0)
    print("{0} received {1} transaction(s)".format(address, len(txouts)))
    for count, txhash in enumerate(txouts):
        print("Transaction {0}".format(count+1))
        print("\ttxhash: {0}".format(txouts[txhash]['txhash']))
        print("\tn: {0}".format(txouts[txhash]['n']))
        print("\tvalue: {0}".format(txouts[txhash]['value']))

def send(wallet):
    account = wallet.getaccount()
    msg = "Enter the id of the address to send coins to"
    toaddress = getaddress(msg, wallet)
    msg = "Enter the balance to transfer to address"
    amount = getamount(msg, min_amount=1)
    balance = 0
    for subaccount in account.itervalues():
        balance = balance + subaccount['balance']
    if balance < amount:
        print("Not enough balance")
        exit(3)
    print("Transferring: {0} to: {1}".format(amount, toaddress))
    wallet.connection.sendtoaddress(toaddress, amount)

def vault_info(wallet):
    vaults = wallet.getvaults()
    print("Vaults")
    if not vaults:
        print("\tNo vaults created yet!")
    for vault in vaults:
        print("Vault Address: {0}".format(vault))
        print("\tBalance: {0}".format(vaults[vault]['balance']))
        print("\tAddress: {0}".format(vaults[vault]['address']))
        print("\tMaster Address: {0}".format(vaults[vault]['master_address']))
        print("\ttimeout: {0} seconds".format(vaults[vault]['timeout']))
        print("\tReceived transactions:")
        if vaults[vault]['received']:
            print("\t\ttxhash: {0}\tn: {1}\tvalue: {2}".format(
                vaults[vault]['received']['txhash'], vaults[vault]['received']['n'], vaults[vault]['received']['value']))
        else:
                print("\t\tNone")

def vault_balance(wallet):
    vaults = wallet.getvaults()
    if not vaults:
        print("No vaults created!")
    for vault in vaults:
        print("{0}: {1}".format(vault, vaults[vault]['balance']))

def vault_new(wallet):
    account = wallet.getaccount()
    toaddress = wallet.getnewaddress()
    tomaster_address = wallet.getnewaddress()
    timeout = 300
    maxfees = 10

    print("Creating new vault ... \nAddress: %s \nMaster address: %s" % \
         (toaddress, tomaster_address))
    vault_address = wallet.newvault(toaddress, tomaster_address, timeout, maxfees)

    if vault_address:
        print("Vault address: {0}".format(vault_address))
    else:
        print("An error occured while creating vault")

def vault_send(wallet):
    account = wallet.getaccount()
    balance = 0
    for subaccount in account.itervalues():
        balance = balance + subaccount['balance']

    vaults = wallet.getvaults()
    emptyvaults = [vault for vault in vaults if not vaults[vault]['balance']]

    if not emptyvaults:
        print("No empty vaults, please create one!")
        exit(1)

    for count, vault in enumerate(emptyvaults):
        print("{0}: {1}".format(count+1, vault))

    msg = "Please enter the index of the vault to transfer money to"
    index = getindex(msg, min_index=1, max_index=len(emptyvaults))
    vault_address = emptyvaults[index-1]
    msg = "Enter the balance to transfer to vault"
    amount = getamount(msg, min_amount=1)

    if balance < amount:
        print("Not enough balance")
        exit(6)

    print("Transfering {0} to vault {1}".format(amount, vault_address))
    ret_value = wallet.sendtovault(vault_address, amount)
    if not ret_value:
        print("An error occured while trasfering")

def vault_withdraw(wallet):
    account = wallet.getaccount()

    vaults = wallet.getvaults()
    nonempty_vaults = [vault for vault in vaults if vaults[vault]['balance']]

    if not nonempty_vaults:
        print("No vaults with available balance")
        exit(1)

    print("Available vaults")
    for n, vault in enumerate(nonempty_vaults):
        print("Id: {0}, Address: {1}, Balance: {2}".format(
            n+1, vaults[vault]["name"], vaults[vault]["balance"]))

    # get from vault
    msg = "Enter the id of the vault you want to transfer coins from"
    index = getindex(msg, min_index=1, max_index=len(nonempty_vaults))
    fromaddress = nonempty_vaults[index-1]

    # get to address
    msg = "Enter the id of the address to send coins to"
    toaddress = getaddress(msg, wallet)

    msg = "Enter the balance to transfer from {0} to {1}".format(fromaddress, toaddress)
    amount = getamount(msg, min_amount=0)
    if vaults[fromaddress]['balance'] < amount + 2:
        print("In sufficient balance in vault, quitting")
        exit(2)

    print("Transfering " + str(amount) + "\tfrom " + fromaddress + "\tto " + toaddress)
    wallet.withdrawfromvault(fromaddress, toaddress, amount)

def vault_override(wallet):
    account = wallet.getaccount()
    toaddress = wallet.getnewaddress()

    transactions = wallet.getpendingtransactions()

    if not transactions:
        print("No pending transactions to override!")
        exit(1)

    print('\nPending Transfers')
    for n, transaction in transactions.iteritems():
        print "\tId: ", n
        print "\t\tInput:", transaction['inputs'][0]
        print "\t\tOutputs: "
        for txout in transaction['outputs']:
            print "\t\t\t", txout['amount'], "->", txout['toaddress']

    msg = "Enter the id of the vault transaction you want to override"
    index = getindex(msg, min_index=1, max_index=len(transactions))
    fromaddress = transactions[str(index)]['inputs'][0]
    print "Fromaddress: ", fromaddress
    print "Toaddress: ", toaddress
    print("Overriding the transaction")
    wallet.overridevault(fromaddress, toaddress)

def vault_fast_withdraw(wallet):
    vaults = wallet.getvaults()
    vaults = list(vaults.itervalues())
    vaults = [vault for vault in vaults if vault['balance']]
    if not vaults:
        print("No vaults available with balance.")
        exit(1)

    # get from vault
    print("Available vaults")
    for n, vault in enumerate(vaults):
        print "Id: ", n+1, vault['name']  + ": ", vault['balance']
    msg = "Enter the id of the vault you want to transfer balance from"
    index = getindex(msg, min_index = 1, max_index = len(vaults))
    fromaddress = vaults[index-1]['name']

    # get to address
    msg = "Enter the id of the address to send coins to"
    toaddress = getaddress(msg, wallet)

    # get amount
    msg = "Enter the balance to transfer from {0} to {1}".format(fromaddress, toaddress)
    amount = getamount(msg, min_amount=0)
    if vaults[index-1]['balance'] < amount + 2:
        print("In sufficient balance in vault, quitting")
        exit(2)

    print("Transfering " + str(amount) + "\tfrom " + fromaddress + "\tto " + toaddress)
    wallet.fastwithdrawfromvault(fromaddress, toaddress, amount)

def vault_pending(wallet):
    transactions = wallet.getpendingtransactions()
    if not transactions:
        print("No pending transactions.")
        exit(1)

    print ('Pending Transfers')
    for n, transaction in transactions.iteritems():
        print "\tId: ", n
        print "\t\tInput:", transaction['inputs'][0]
        print "\t\tOutputs: "
        for txout in transaction['outputs']:
            print "\t\t\t", txout['amount'], "->", txout['toaddress']


def run(args):
    try:
        wallet = Wallet(config_file=args.config_file)
        globals()[args.command](wallet)
    except TransportException as e:
        print str(e)
        sys.exit(1)

    sys.exit(0)

# any function added above should be registered here
_SUPPORTED_COMMANDS = [
    ("account", "Look at the account summary.",),
    ("balance", "Current wallet balance.",),
    ("blockchain", "Dump the current block chain.",),
    ("info", "Get basic info",),
    ("mempool", "Dump the mempool.",),
    ("newaddress", "Generate a new address.",),
    ("received", "Received transactions.",),
    ("send", "Send coins to normal address.",),
    ("vault_info", "Detailed information about the vaults.",),
    ("vault_new", "Create a new vault account"),
    ("vault_send", "Send to a vault.",),
    ("vault_balance", "Balance in each vault account."),
    ("vault_withdraw", "Withdraw from a vault.",),
    ("vault_override", "Override a vault transaction.",),
    ("vault_fast_withdraw", "Withdraw from a vault immediately. No timeout associated.",),
    ("vault_pending", "List of pending vault transactions.",),
    ]

_EPILOG = "Commands Desription:\n====================\n"
for cmd, hlp in _SUPPORTED_COMMANDS:
    _EPILOG += "{:<30} {}\n".format(cmd, hlp)

_EPILOG += """
In addition, you can pass in the config-file to be used.
By default, it is ~/.reversecoin.cfg
"""

_WALLET_NAME = """
ReverseCoin Wallet - v%s

Copyright: %s
""" % (VERSION, COPYRIGHT_YEAR)

def parse_arguments():

    parser = argparse.ArgumentParser(description=_WALLET_NAME,
                                     epilog=_EPILOG,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=[c for c,_ in _SUPPORTED_COMMANDS])
    parser.add_argument("config_file", nargs='?', default='~/.reversecoin.cfg')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

def main():
    args = parse_arguments()
    run(args)

if __name__ == "__main__":
    main()
