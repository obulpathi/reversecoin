#!/usr/bin/python
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from datetime import datetime
from datetime import timedelta
import logging
import sqlite3 as sqlite
import copy
import os
import binascii

from bitcoin import script
import utils


class VaultDB(object):
    def __init__(self, datadir):
        self.vaultfile = os.path.expanduser(datadir + '/vault.db')
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        # create sqlitedb, if its does not exist
        connection = sqlite.connect(self.vaultfile)
        cursor = connection.cursor()
        # create vaults table
        cmd = "CREATE TABLE vaults (txhash varchar(100), fromaddress varchar(100), datetime DATE)"
        cursor.execute(cmd)
        self.logger.debug('Created VaultDB')
        connection.commit()
        connection.close()

    def addvaulttxs(self, txs):
        # add transactions to VaultDB
        self.logger.debug('Adding transactions to VaultDB')
        connection = sqlite.connect(self.vaultfile)
        cursor = connection.cursor()
        cmd = "INSERT INTO vaults VALUES(?, ?, ?)"
        for tx in txs:
            values = (str(tx.sha256), str(utils.tx_to_vault_address(tx)),
                datetime.now() + timedelta(seconds=20)) #FIXME
            cursor.execute(cmd, values)
        connection.commit()
        connection.close()
        self.logger.debug('Added transactions to VaultDB')

    def removeconfirmedvaulttxs(self, txs):
        if not txs:
            return
        # remove confirmed transactions from VaultDB
        self.logger.debug('Removing confirmed transactions from VaultDB')
        connection = sqlite.connect(self.vaultfile)
        cursor = connection.cursor()
        cmd_confirmed = "DELETE FROM vaults WHERE txhash = (?)"
        cmd_override = "DELETE FROM vaults WHERE fromaddress = (?)"
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
                    cursor.execute(cmd_confirmed, values)
                    #break
                if txin.scriptSig[0] == chr(script.OP_VAULT_OVERRIDE):
                    fromaddress = str(utils.scriptSig_to_vault_address(txin.scriptSig))
                    values = (fromaddress,)
                    cursor.execute(cmd_override, values)
        connection.commit()
        connection.close()
        self.logger.debug('Removed confirmed transactions from VaultDB')

    def addblock(self, block):
        self.listpendingtxs()
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
        self.listpendingtxs()
        self.addvaulttxs(new_txs)
        self.listpendingtxs()

    def getpendingvaulttxs(self):
        txs = []
        connection = sqlite.connect(self.vaultfile)
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
        connection = sqlite.connect(self.vaultfile)
        cursor = connection.cursor()
        cmd = "SELECT * FROM vaults WHERE (?) > datetime"
        values = (datetime.now(),)
        cursor.execute(cmd, values)
        for entry in cursor:
            txs.append(int(entry[0]))
        connection.close()
        return txs

    def listpendingtxs(self):
        connection = sqlite.connect(self.vaultfile)
        cursor = connection.cursor()
        cmd = "SELECT * FROM vaults"
        cursor.execute(cmd)
        for entry in cursor:
            self.logger.debug('{0} {1} {2}'.format(entry[0], entry[1], entry[2]))
        connection.close()
