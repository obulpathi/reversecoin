reversecoind:
	python reversecoin/reversecoin.py etc/config.cfg

reversecoinminer:
	python reversecoin/miner/miner.py etc/miner.cfg

cleanconfig:
	rm ~/.reversecoin.cfg
	rm ~/.reversecoin.cfg

cleandata:
	rm -rf ~/.reversecoin

clean:
	make cleanconfig
	make cleandata
