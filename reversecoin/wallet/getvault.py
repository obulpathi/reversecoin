import bitcoinrpc

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
