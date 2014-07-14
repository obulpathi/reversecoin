import bitcoinrpc

# JSON-RPC server user, password.  Uses HTTP Basic authentication.
rpcuser = "user"
rpcpass = "passwd"

connection = bitcoinrpc.connect_to_remote(rpcuser, rpcpass, host='localhost', port=9333, use_https=False)
vault = connection.getvault()
print "Name: ", vault['name']
print "Address: ", vault['address']
print "Master Address: ", vault['master_address']
#print "Public key: ", vault['public_key']
#print "Private key: ", vault['private_key']
#print "Master Public key: ", vault['master_public_key']
#print "Master Private key: ", vault['master_private_key']
print "Balance: ", vault['amount']
