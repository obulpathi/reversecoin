timevaultd:
	python timevault/bitcoinpy.py etc/config.cfg

vaultminer:
	python timevault/miner/miner.py etc/miner.cfg

clean:
	rm -rf ~/.bitcoinpy
