import sys
import argparse

from timevault.wallet.wallet import Wallet
from timevault import bitcoinrpc

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
        for txouts in transaction['outputs']:
            print txouts['toaddress'] + ": ", txouts['amount']

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
    
    address = sys.argv[1]
    
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
        print "\tInputs: "
        for txin in transaction['inputs']:
            print "\t\t", txin
            print "\tOutputs: "
        for txout in transaction['outputs']:
            print "\t\t", txout
                    
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
    for transaction in transactions:
        for txouts in transaction['outputs']:
            print txouts['toaddress'] + ": ", txouts['amount']

def run(args):

    if args.address:
        address()
    elif args.account:
        account()
    elif args.balance:
        balance()
    elif args.getvaults:
        getvaults()
    elif args.blockchain:
        blockchain()
    elif args.mempool:
        mempool()
    elif args.received:
        received()
    elif args.send:
        send()
    elif args.getvault:
        getvault()
    elif args.savings:
        savings()
    elif args.vault_send:
        vault_send()
    elif args.vault_withdraw:
        vault_withdraw()
    elif args.vault_override:
        vault_override()
    elif args.vault_fast_withdraw:
        vault_fast_withdraw()
    elif args.vault_pending:
        vault_pending()

def parse_arguments():

    parser = argparse.ArgumentParser(description="Timevault client version 1.0.0",
                                     argument_default=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("address", help="Generate a new address.", nargs='?')
    group.add_argument("account", help="Look at the account summary.", nargs='?')
    group.add_argument("balance", help="Current wallet balance.", nargs='?')
    group.add_argument("getvaults", help="Information about the vaults.", nargs='?')
    group.add_argument("blockchain", help="Dump the current block chain.", nargs='?')
    group.add_argument("mempool", help="Dump the mempool.", nargs='?')
    group.add_argument("received", help="Received transactions.", nargs='?')
    group.add_argument("send", help="Send coins.", nargs='?')
    group.add_argument("getvault", help="", nargs='?')
    group.add_argument("savings", help="", nargs='?')
    group.add_argument("vault_send", help="", nargs='?')
    group.add_argument("vault_withdraw", help="", nargs='?')
    group.add_argument("vault-override", help="", nargs='?')
    group.add_argument("vault_fast_withdraw", help="", nargs='?')
    group.add_argument("vault_pending", help="", nargs='?')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()

def main():
    args = parse_arguments()
    run(args)

if __name__ == "__main__":
    main()
