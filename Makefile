
help:
	@py -c "print('\n'.join(filter(lambda x: ':' in x and '@' not in x, open('Makefile').read().split('\n'))))"

run:
	py main.py

install:
	pip3 install -r requirements.txt