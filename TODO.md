TODO
====

FEATURES
--------
* Add documentation and notes
* Mark the bugs with #FIXME tag
* Installation and documentation for installation
* Initialization and documentation for initialization
* Validate transactions
* Transaction and Block Propagation
* VaultDB as a separate file
* VaultChain in a separate file
* Redo code layout
* Add test cases
* Installation using python wheels
* Support for pay to script hash
* Support for multisig transactions
* Grammar and spell check
* Wallet compatibility
* Support for stratum miner
* Support for all RPC function calls
* PEP8 and flake check
* See BUGS for miscellaneous fixes
* Lightweight
* Modular
* Mining Pool
* Exchange
* Monitoring System
* Hardware Wallet

CLEANUP:
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
