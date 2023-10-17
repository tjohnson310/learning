EMPTY = None

a = [[EMPTY, EMPTY, EMPTY],
     [EMPTY, EMPTY, EMPTY],
     [EMPTY, EMPTY, EMPTY]]

if EMPTY not in [item for sublist in a for item in sublist]:
    print(True)
else:
    print(False)
