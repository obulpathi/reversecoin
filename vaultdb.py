#!/usr/bin/python
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from datetime import datetime
from datetime import timedelta
import logging
import sqlite3 as sqlite
import copy

from bitcoin import script


class VaultDB(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)


    def initialize(self):
        # create sqlitedb, if its does not exist
        connection = sqlite.connect('vault.db')
        cursor = connection.cursor()
        # create vaults table
        cmd = "CREATE TABLE vaults (txhash varchar(100), datetime DATE)"
        cursor.execute(cmd)
        self.logger.debug('Created VaultDB')
        connection.commit()
        connection.close()

    def addvaulttxs(self, txs):
        # add transactions to VaultDB
        self.logger.debug('Adding transactions to VaultDB')
        connection = sqlite.connect('vault.db')
        cursor = connection.cursor()
        cmd = "INSERT INTO vaults VALUES(?, ?)"
        for tx in txs:
            print tx.sha256, type(tx.sha256)
            values = (str(tx.sha256),
                datetime.now() + timedelta(seconds=10000)) #FIXME
            cursor.execute(cmd, values)
        connection.commit()
        connection.close()
        self.logger.debug('Added transactions to VaultDB')

    def removeconfirmedvaulttxs(self, txs):
        if not txs:
            return
        # remove confirmed transactions from VaultDB
        self.logger.debug('Removing confirmed transactions from VaultDB')
        connection = sqlite.connect('vault.db')
        cursor = connection.cursor()
        cmd = "DELETE FROM vaults WHERE txhash = (?)"
        for tx in txs:
            if tx.is_coinbase():
                continue
            new_tx = copy.deepcopy(tx)
            for txin in new_tx.vin:
                # if this is confirmed vault transaction, add it to confirmed txs
                if txin.scriptSig[0] == chr(script.OP_VAULT_CONFIRM):
                    txin.scriptSig = chr(script.OP_VAULT_WITHDRAW) + txin.scriptSig[1:]
                    new_tx.calc_sha256()
                    values = (str(new_tx.sha256),)
                    cursor.execute(cmd, values)
                    #break
                if txin.scriptSig[0] == chr(script.OP_VAULT_OVERRIDE):
                    # get the original pending transaction
                    # by referring the previous hash and then delete it
                    raise NotImplementedError
        connection.commit()
        connection.close()
        self.logger.debug('Removed confirmed transactions from VaultDB')

    def addblock(self, block):
        new_txs = []
        confirmed_txs = []
        for tx in block.vtx:
            for txin in tx.vin:
                # if this is a vault initiate transaction, add it to new txs
                if txin.scriptSig and txin.scriptSig[0] == chr(script.OP_VAULT_WITHDRAW):
                    new_txs.append(tx)
                # if this is confirmed vault transaction, add it to confirmed txs
                if txin.scriptSig and txin.scriptSig[0] == chr(script.OP_VAULT_CONFIRM):
                    confirmed_txs.append(tx)
                # if this is override vault transaction, add it to confirmed txs
                if txin.scriptSig and txin.scriptSig[0] == chr(script.OP_VAULT_OVERRIDE):
                    confirmed_txs.append(tx)
        self.removeconfirmedvaulttxs(confirmed_txs)
        self.addvaulttxs(new_txs)

    def getpendingvaulttxs(self):
        txs = []
        connection = sqlite.connect('vault.db')
        cursor = connection.cursor()
        cmd = "SELECT * FROM vaults WHERE (?) < datetime"
        values = (datetime.now(),)
        cursor.execute(cmd, values)
        for entry in cursor:
            txs.append(int(entry[0]))
        connection.close()
        return txs

    def getconfirmedvaulttxs(self):
        txs = []
        connection = sqlite.connect('vault.db')
        cursor = connection.cursor()
        cmd = "SELECT * FROM vaults WHERE (?) > datetime"
        values = (datetime.now(),)
        cursor.execute(cmd, values)
        for entry in cursor:
            txs.append(int(entry[0]))
        connection.close()
        return txs
