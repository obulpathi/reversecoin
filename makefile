reversecoind:
	python reversecoin/reversecoinpy.py etc/config.cfg

reversecoin-miner:
	python reversecoin/miner/miner.py etc/miner.cfg

cleanconfig:
	rm ~/.reversecoin.cfg
	rm ~/.reversecoin.cfg

clean:
	rm -rf ~/.reversecoin

cleanall:
	make clean
	make cleanconfig
