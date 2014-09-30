# MemPool.py
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
import logging

from bitcoin.serialize import uint256_to_shortstr


class MemPool(object):
	def __init__(self):
		self.pool = {}
		self.prevouts = set()
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
		prevouts = set()
		for txin in tx.vin:
			if txin.prevout.hash in self.prevouts:
				self.logger.error(
					"MemPool.add{0}: tx already spent".format(txin.prevout.hash))
				return False
			prevouts.add(txin.prevout.hash)
		for txhash in prevouts:
			self.prevouts.add(txhash)
		self.pool[hash] = tx
		self.logger.debug("MemPool.add(%s), poolsz %d" % (hashstr, len(self.pool)))
		return True

	def remove(self, hash):
		if hash not in self.pool:
			return False
		tx = self.pool[hash]
		for txin in tx.vin:
			self.prevouts.remove(txin.prevout.hash)
		del self.pool[hash]
		return True

	def size(self):
		return len(self.pool)

	def dumpmempool(self):
		print "mempool"
		for txhash in self.pool:
			print "txhash: {0}".format(txhash)
		print "prevouts"
		for txhash in self.prevouts:
			print "txhash: {0}".format(txhash)
