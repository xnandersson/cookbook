with open('mycert.des', 'rb') as f:
    byte = f.read(1)
    index = 0
    print(f'{index:04x} ', end='')
    while byte:
        print('%02x ' % byte[0], end='')
        index += 1
        if index % 20 == 0:
            print(f'\n{index:04x} ', end='') 
        byte = f.read(1)
    print('\n')
