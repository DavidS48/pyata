from sands.pd_obj import PdObj, PdMess, SubPatch
from sands.Pd import Pd 
from time import sleep

pd = Pd()
pd.init()



def amp_mod():
    sig_in = PdObj("inlet~")
    rate_in = PdObj("inlet")
    osc = PdObj("osc~")
    out = PdObj("outlet~")
    osc.i0 << rate_in.o0
    out.i0 << osc.o0 * sig_in.o0
    print("Created.")


freq = PdMess("440")
rate = PdMess("660")
osc = PdObj("osc~")
#sleep(4)
print("subpatching")
am = SubPatch("am", amp_mod)
print("done")
#sleep(2)
out = PdObj("dac~")
osc.i0 << freq.o0
am.i1 << osc.o0
am.i0 << rate.o0
freq.click()
rate.click()
out.i0 << am.o0

_ = input("Quit?")
pd = pd.quit()


