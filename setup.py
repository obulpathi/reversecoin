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

_PKG_ROOT = 'timevault'

setuptools.setup(
    name = _PKG_ROOT,
    install_requires=reqs,
    packages = [_PKG_ROOT] + [_PKG_ROOT+'.'+p for p in setuptools.find_packages(_PKG_ROOT)],
    entry_points = {
        'console_scripts': ['timevaultd=timevault.bitcoinpy:run',
			    'timevaultclient=timevault.wallet.timevaultclient:main',
                            'vaultminer=timevault.miner.miner:run'],},
    version = "1.0.0", # TODO: Fix this
    description = "A secure revertible crypto currency",
    url = "https://vaultcoin.org",
    author = "Obulpathi N Challa",
    author_email = "obulpathi@gmail.com",
    zip_safe = False,
)
