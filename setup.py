import os
import shutil
import setuptools
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

# copy configuration files
shutil.copy('etc/config.cfg', os.path.expanduser('~/.bitcoinpy.cfg'))
shutil.copy('etc/miner.cfg', os.path.expanduser('~/.vaultminer.cfg'))

"""
def initialize(datadir = "/home/obulpathi/.bitcoinpy"):
    os.mkdir(datadir)
    os.mkdir(datadir + '/leveldb')
    # create blocks.dat file
    shutil.copy(os.path.expanduser('~/.genesis.dat'), \
        os.path.join(datadir + '/blocks.dat'))
    # create lock file for db
    with open(datadir + '/__db.001', 'a'):
        pass

initialize()
"""

setuptools.setup(
    install_requires=reqs,
    entry_points = {
        'console_scripts': ['timevaultd=timevault.bitcoinpy:run',
                            'vaultminer=timevault.miner.miner:run'],}
)
