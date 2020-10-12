# Makefile for Python

PYTHON       = python3

server:
	python file-transfer-lab/fileServer.py

client:
	python file-transfer-lab/main.py

proxy:
	python file-transfer-lab/lib/stammerProxy.py

clientP:
	python file-transfer-lab/main.py -s 127.0.0.1:50001
