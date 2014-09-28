Bitcoinpy
=========

Bitcoinpy is a Python implementation of Bitcoin to help understand the internals of Bitcoin easy.


Bitcoinpy project is aimed at developers who want to learn about the internal workings of Bitcoin. We created this project so it it is easy to read, understand and modify Bitcoin. Bitcoinpy was developed in Python, so that someone with a little bit of programming ability can read and understand the inner workings of Bitcoin. Lots of helpful documentation is provided to help understand the higher level workings of system and its components. Project is implemented in a very modular fashion, so that if someone wants to change the functionality of a component, they can change or replace that particular component and reuse the rest of the code to test their change without lot of changes. Additional tools like the code for creating genesis block, creating and signing transactions, dumping information from blocks, analyzing the blockchain and other debugging tools have been provided to help developers easily bootstrap and debug new alt coins.

In order to keep the code lightweight we reused the libraries including the Bitcoinlib by Jeff Garzik and others. Code contains all the components including the full bitcoin client, server, wallet and miner. However, some of the components like P2SH, alert messages and more are missing. We will add support for missing functionality, albeit slowly. if you would like to contribute, please feel free to fork the project, hack it and send a pull request. We will gladly accept your changes. Any contributions including documentation are welcome.

How to install on Ubuntu
------------------------
* Install dependencies: sudo apt-get install python-dev libleveldb1 python-gevent python-leveldb python-bsddb3 python-sqlite
* After installing dependencies, install bitcoinpy usinf "python setup.py install"

How to run tests
----------------
Bitcoinpy uses tox and nose for testing. To run tests, simply cd into bitcoinpy folder and enter the command "tox". Selective tests can be run using the command "$ tox -- tests.api.test_wallet:TestWallet.test_info". If you want to start timevaultd and vaultminer for manual testing, enter into virtualenv by using "source bitcoinpy/.tox/py26/bin/activate", then run the commands timevaultd for running the timevault daemon and vaultminer for mining coins.
