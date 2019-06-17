import time
import random

from sands.pd_obj import PdObj, PdNum
from sands.Pd import Pd 
from sands.tidy_patch import tidy_patch

pd = Pd()
pd.init()

freq = PdNum(440)
osc1 = PdObj("osc~")
osc2 = PdObj("osc~")
dac = PdObj("dac~")

dac.i0 << osc1.o0 + osc2.o0
osc1.i0 << freq.o2
osc2.i0 << freq.o0 * 2
tidy_patch(dac)
time.sleep(10)
pd.quit()
sys.exit()

for _ in range(100):
    next_freq = random.randrange(220, 880)
    freq.set(next_freq)
    time.sleep(220 / next_freq)


pd.quit()
