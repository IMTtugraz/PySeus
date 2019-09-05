from context import pyseus

import tracemalloc

tracemalloc.start()

# pyseus.load("test.h5")
pyseus.load("dicom/VFA_Prob01_23_05_2018/20180523_18.05.23-15_38_07-DST-1.3.12.2.1107.5.2.19.45250_1/RAVE_longRF_3deg/VFA_Prob010201030001000100010001.DCM")

snapshot = tracemalloc.take_snapshot()

print("Memory Test\n===========\n")
for s in snapshot.statistics('filename'):
    print("{} Byte in {}".format(s.size, s.traceback))
