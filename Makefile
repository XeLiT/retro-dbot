
run:
	py sniffer/main.py

install:
	pip3 install -r requirements.txt

test_map:
	py sniffer/frames/map_frame.py