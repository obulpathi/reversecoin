import bitcoinrpc

class Wallet(object):
    def __init__(self):
        # JSON-RPC server user, password.
        # Uses HTTP Basic authentication.
        rpcuser = "user"
        rpcpass = "passwd"
        account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)

    def getaccount(self, account = "account"):
        account = self.connection.getaccount(account)
        return account

    def getvaults(self):
        vaults = self.connection.getvaults()
        return vaults

    def getpendingtransactions(self):
        return self.connection.getpendingtransactions()

    def sendtovault(self, toaddress, tomaster_address, timeout, amount):
        self.connection.sendtovault(toaddress, tomaster_address, timeout, amount)

    def withdrawfromvault(self, fromaddress, toaddress, amount):
        self.connection.withdrawfromvault(fromaddress, toaddress, amount)

    def fastwithdrawfromvault(self, fromaddress, toaddress, amount):
        self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)
