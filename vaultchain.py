#!/usr/bin/python
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

class VaultChain(object):
    def __init__(self):
        # create sqlitedb, if its does not exist
        connection = sqlite3.connect('vaultchain.db')
        cursor = connection.cursor()
        # create vaultchaindb, if its does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS vaultchain
                      (txhash varchar(50), date text)''')
        connection.commit()
        connection.close()

    def addvaulttx(self, tx):
        # add a transaction to VaultChainDB
        connection = sqlite3.connect('vaultchain.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO vaults VALUES(" + \
                        str(tx.sha256) + "," + datetime() + timeout))
        connection.commit()
        connection.close()

    def getvaulttx(self):
        raise NotImplementedError
