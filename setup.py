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

setuptools.setup(
    name = "timevault",
    install_requires=reqs,
    packages = ["timevault",
                "timevault.bitcoin",
                "timevault.bitcoinrpc",
                "timevault.miner",
                "timevault.others",
                "timevault.tools",
                "timevault.wallet"],
    entry_points = {
        'console_scripts': ['timevaultd=timevault.bitcoinpy:run',
                            'vaultminer=timevault.miner.miner:run'],},
    version = "1.0.0", # TODO: Fix this
    description = "A secure revertible crypto currency",
)
