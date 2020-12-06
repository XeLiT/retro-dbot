help:
	@py -c "print('\n'.join(filter(lambda x: ':' in x and '@' not in x, open('Makefile').read().split('\n'))))"

install:
	pip3 install -r requirements.txt

test:
	py main_test.py

run:
	py main.py
