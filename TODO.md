TODO
====

BUGS
----
* Migrate minimum fee check to client side
* Enforce single vault per address
* Check for vault override and vault confirm in same block:
  Enforce vault override and vault confirm does not happen together (new block creation)
* Enforce that a vault override will not happen, if there is no balance / vault
  confirm happened
* Vault Address format: scriptSig to vault address
* If same address appears in output tx twice, one txout is getting
  overwritten in chaindb:listreceivedbyaddress
* Fix FIXMEs

FEATURES
--------
* Add test cases
* Transaction and Block Propagation
* Validate transactions
* Installation using python wheels
* Documentation for installation
* PEP8 and flake check
* Add documentation and notes
* Support for pay to script hash
* Support for multisig transactions
* Vault rate control
* Wallet compatibility
* Support for stratum miner
* Mining Pool
* Exchange
* Monitoring System
* Hardware Wallet

NAME and ICON
-------------
* Vaultcoin: Already taken, but we have www.vaultcoin.net
* Time Travel Coin: No one had used .. but will it signify Security?

LATER
-----
* Wallet Transistion from bsddb to SQLite?
* Single database for Wallet and Vault transactions?

Evaluate this checklist
-----------------------
https://en.bitcoin.it/wiki/Protocol_rules#.22block.22_messages
