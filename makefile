all:
	python bitcoinpy.py config.cfg

clean:
	rm -rf ~/.bitcoinpy
	rm -f wallet/vault.db

new:
	rm -rf ~/.bitcoinpy/*
	rm -f wallet/vault.db
	mkdir -p ~/.bitcoinpy/leveldb
	cp genesis.dat ~/.bitcoinpy/blocks.dat
	python bitcoinpy.py config.cfg

install:
	sudo apt-get install python-gevent libleveldb1 python-leveldb python-bsddb3 python-sqlite 
