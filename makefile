all:
	python bitcoinpy.py config.cfg

debug:
	python -m pdb bitcoinpy.py config.cfg

test:
	python test.py

tmp:
	python tmp.py

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
	sudo apt-get install python-gevent libleveldb1 python-leveldb python-bsddb3 
