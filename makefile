all:
	python bitcoinpy.py config.cfg

clean:
	rm -rf ~/.bitcoinpy
	rm -f vault.db

install:
	sudo apt-get install python-dev libleveldb1
	sudo apt-get install python-gevent python-leveldb python-bsddb3 python-sqlite
