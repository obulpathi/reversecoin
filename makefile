timevaultd:
	python timevault/bitcoinpy.py etc/config.cfg

vaultminer:
	python timevault/miner/miner.py etc/miner.cfg

cleanconfig:
	rm ~/.bitcoinpy.cfg
	rm ~/.vaultminer.cfg

cleandata:
	rm -rf ~/.bitcoinpy

clean:
	make cleanconfig
	make cleandata
