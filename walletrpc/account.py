import bitcoinrpc

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser = "user"
rpcpass = "passwd"
account = "account"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
account = connection.getaccount(account)
for subaccount in account.itervalues():
    print "Address: ", subaccount['address']
    print "Public key: ", subaccount['public_key']
    print "Private key: ", subaccount['private_key']
    print "Balance: ", subaccount['balance']
    print "\n\n"
