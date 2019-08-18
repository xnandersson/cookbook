class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open('mycert.des', 'rb') as f:
    byte = f.read(1)
    index = 0
    print(f'{index:04x} ', end='')
    colorize = False
    while byte:
        if byte[0] == 0x30:
            print(bcolors.FAIL, end='')
            colorize = True
        print('%02x ' % byte[0], end='')
        if colorize:
            print(bcolors.ENDC, end='')
            colorize = False
        index += 1
        if index % 20 == 0:
            print(f'\n{index:04x} ', end='') 
        byte = f.read(1)
    print('\n')
