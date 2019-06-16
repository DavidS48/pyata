
from pd_obj import PdObj, PdNum
from Pd import Pd 
import time
import random

pd = Pd()
pd.init()

freq = PdNum(440)
osc = PdObj("osc~")
dac = PdObj("dac~")

dac.i0 << osc.o0
osc.i0 << freq.o0

for _ in range(100):
    next_freq = random.randrange(220, 880)
    freq.set(next_freq)
    time.sleep(220 / next_freq)

dac.i0 | osc.o0

pd.quit()
