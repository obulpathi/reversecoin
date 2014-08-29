# coredefs.py
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from __future__ import absolute_import, division, print_function, unicode_literals

PROTO_VERSION = 60002

CADDR_TIME_VERSION = 31402

MIN_PROTO_VERSION = 209

BIP0031_VERSION = 60000

NOBLKS_VERSION_START = 32000
NOBLKS_VERSION_END = 32400

MEMPOOL_GD_VERSION = 60002

COIN = 100000000
MAX_MONEY = 21000000 * COIN

def MoneyRange(nValue):
    return 0<= nValue <= MAX_MONEY

class NetMagic(object):
    def __init__(self, msg_start, block0, checkpoints):
        self.msg_start = msg_start
        self.block0 = block0
        self.checkpoints = checkpoints

        self.checkpoint_max = 0
        for height in self.checkpoints.keys():
            if height > self.checkpoint_max:
                self.checkpoint_max = height

NETWORKS = {
 'mainnet' : NetMagic(b"\xf9\xbe\xb4\xd9",
    0x2470ad8edc16062e2baa5fc3acb3e3f719d21dfc35d927ba8972fe3e3790acff,
    {
     0: 0x2470ad8edc16062e2baa5fc3acb3e3f719d21dfc35d927ba8972fe3e3790acff,
    }),
 'testnet3' : NetMagic(b"\x0b\x11\x09\x07",
        0x0000006e52799ec0e71289b7a4f60dd2e0d9fde649f9f9cd3725e91f65fd23b9,
    {
     0: 0x0000006e52799ec0e71289b7a4f60dd2e0d9fde649f9f9cd3725e91f65fd23b9,
    })
}
