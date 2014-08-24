TODO
====

BUGS
----
* If same address appears in output tx twice, one txout is getting
  overwritten in chaindb:listreceivedbyaddress
* Enforce single Vault or Support multiple Vaults per address pair
* Migrate minimum fee check to client side
* Check for vault override and vault confirm in same block
* Enfore vault override and vault confirm does not happen together (new block creation)
* Enfore that a vault override will not happen, if there is no balance / vault confir happened
* Remove hardcoded fees
* Remove hardcoded timeout for vault
* Immediate flush and sync of blockchain upon block generation
* One source for all kind of wallet questions
* Vault Address format: scriptSig to vault address
* Pending and active balance at the same time
* Fix FIXMEs

FEATURES
--------
* Validate transactions
* Transaction and Block Propagation
* CLEANUP and BUGS
* Redo code layout
* Installation using python wheels
* Add documentation and notes
* Documentation for installation
* PEP8 and flake check
* Add test cases
* Support for pay to script hash
* Support for multisig transactions
* Vault rate control
* Wallet compatibility
* Support for stratum miner
* Support for all RPC function calls
* Run server only on localhost
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
