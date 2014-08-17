TODO
====

FEATURES
--------
* VaultDB as a separate file
* VaultChain in a separate file
* Validate transactions
* Transaction and Block Propagation
* CLEANUP and BUGS
* Redo code layout
* Installation using python wheels
* Grammar and spell check
* Add documentation and notes
* Documentation for installation
* Documentation for initialization
* PEP8 and flake check
* Add test cases
* Support for pay to script hash
* Support for multisig transactions
* Wallet compatibility
* Support for stratum miner
* Support for all RPC function calls
* Mining Pool
* Exchange
* Monitoring System
* Hardware Wallet

CLEANUP
-------
* Fix hash and scriptSig formats
* Fix tx hash and block hash for vault_fastwithdraw in chaindb and wallet

BUGS
----
* Remove hardcoded fees
* Remove hardcoded timeout for vault
* Multiple vault support
* Enforce single Vault or Support multiple Vaults per address pair
* If same address appears in output tx twice, one txout is getting
  overwritten in chaindb:listreceivedbyaddress
* Fix FIXMEs

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
