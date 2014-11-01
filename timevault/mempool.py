# MemPool.py
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
import logging

from bitcoin.serialize import uint256_to_shortstr
import utils

class MemPool(object):
	def __init__(self):
		self.pool = {}
		# setup logging
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)

	def add(self, tx):
		tx.calc_sha256()
		hash = tx.sha256
		hashstr = uint256_to_shortstr(hash)
		if hash in self.pool:
			self.logger.warning("MemPool.add(%s): already known" % (hashstr,))
			return False
		if not tx.is_valid():
			self.logger.error("MemPool.add(%s): invalid TX" % (hashstr, ))
			return False
		self.pool[hash] = tx
		self.logger.debug("MemPool.add(%s), poolsz %d" % (hashstr, len(self.pool)))
		return True

	def remove(self, hash):
		if hash not in self.pool:
			return False
		del self.pool[hash]
		return True

	def size(self):
		return len(self.pool)

	def hasvault(self, vault_address):
		script = utils.vault_address_to_pay_to_vault_script(vault_address)
		for txhash in self.pool:
			if self.pool[txhash].vout[0].scriptPubKey == script:
				return True
		return False

	def dumpmempool(self):
		print "mempool"
		for txhash in self.pool:
			print "txhash: {0}".format(txhash)
