HEX_CHARS = "0123456789ABCDEF"
ZKARRAY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SUN_MAGICS = [1030, 1029, 4088]
MAP_WIDTH = 15
MAP_HEIGHT = 33

RED = lambda x: '\033[1;31m{}\033[0m'.format(x)
YELLOW = lambda x: '\033[0;33m{}\033[0m'.format(x)
DIM = lambda x: '{}'.format(x)