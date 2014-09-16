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
* Installation using python wheels
* Documentation for installation
* Fix FIXMEs

FEATURES
--------
* Transaction and Block Propagation
* Validate transactions
* Wallet compatibility
* Support for pay to script hash (P2SH)
* Support for multisig transactions
* Support for stratum miner
* Add test cases
* Add documentation and notes
* PEP8 and flake check
* Monitoring System
* Steal my coins challenge
* Hardware Wallet
* Mining Pool
* Exchange

OTHERS
------
* If same address appears in output tx twice, one txout is getting
  overwritten in chaindb:listreceivedbyaddress

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
