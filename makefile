all:
	python timevault/bitcoinpy.py etc/config.cfg

clean:
	rm -rf ~/.bitcoinpy
