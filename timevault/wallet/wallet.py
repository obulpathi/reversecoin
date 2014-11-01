from timevault import bitcoinrpc

class Wallet(object):
    def __init__(self):
        # JSON-RPC server user, password.
        # Uses HTTP Basic authentication.
        rpcuser = "user"
        rpcpass = "passwd"
        account = "account"
        self.connection = bitcoinrpc.connect_to_remote(
            rpcuser, rpcpass, host='localhost', port=9333, use_https=False)

    def dumpblockchain(self):
        self.connection.dumpblockchain()

    def dumpmempool(self):
        self.connection.dumpmempool()

    def getaccount(self, account = "account"):
        account = self.connection.getaccount(account)
        return account

    def getnewaddress(self, account = "account"):
        address = self.connection.getnewaddress(account)
        return address

    def getvaults(self):
        vaults = self.connection.getvaults()
        return vaults

    def getpendingtransactions(self):
        return self.connection.getpendingtransactions()

    def newvault(self, toaddress, tomaster_address, timeout, maxfees):
        return self.connection.newvault(toaddress, tomaster_address, timeout, maxfees)

    def send(self, toaddress, amount):
        self.connection.sendtoaddress(toaddress, amount)

    def sendtovault(self, toaddress, tomaster_address, amount, timeout, maxfees):
        return self.connection.sendtovault(toaddress, tomaster_address, amount, \
            timeout, maxfees)

    def withdrawfromvault(self, fromaddress, toaddress, amount):
        return self.connection.withdrawfromvault(fromaddress, toaddress, amount)

    def overridevault(self, fromaddress, toaddress):
        return self.connection.overridevaulttx(fromaddress, toaddress)

    def fastwithdrawfromvault(self, fromaddress, toaddress, amount):
        return self.connection.fastwithdrawfromvault(fromaddress, toaddress, amount)
