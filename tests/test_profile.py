from context import pyseus

from datetime import datetime
import cProfile
import io
import pstats

# @see https://qxf2.com/blog/saving-cprofile-stats-to-a-csv-file/

profile = cProfile.Profile()
profile.enable()

# pyseus.load('test.h5')
pyseus.load("dicom/VFA_Prob01_23_05_2018/20180523_18.05.23-15_38_07-DST-1.3.12.2.1107.5.2.19.45250_1/RAVE_longRF_3deg/VFA_Prob010201030001000100010001.DCM")

profile.disable()

result = io.StringIO()
pstats.Stats(profile, stream=result).print_stats()
result = result.getvalue()

result = 'ncalls'+result.split('ncalls')[-1]
result = '\n'.join([','.join(line.rstrip().split(None,5)) for line in result.split('\n')])

with open('profile.csv', 'w+') as f:
    f.write(result)
    f.close()
