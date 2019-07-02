
from sands.pd_obj import PdObj, PdNum, PdMess, SubPatch, PdInlet, PdMInlet, PdOutlet
from sands.Pd import Pd
from sands.sequencer import ValueSequencer

pd = Pd()
pd.init()

def simple_env():
    dec_in = PdInlet()
    trigger = PdMInlet()
    delay = PdObj("delay 20")
    att = PdMess("1 20")
    dec_inst = PdObj("snapshot~")
    zero = PdMess("0")
    dec = PdObj("pack 0 400")
    line = PdObj("line")
    pr = PdObj("print")
    out = PdOutlet()
    att.i0 << trigger.o0
    delay.i0 << trigger.o0
    dec_inst.i0 << dec_in.o0
    dec_inst.i0 << delay.o0
    pr.i0 << dec_inst.o0
    zero.i0 << delay.o0
    dec.i0 << zero.o0
    dec.i1 << dec_inst.o0
    line.i0 << att.o0
    line.i0 << dec.o0
    out.i0 << line.o0

note = PdNum(69)
trigger = PdMess("bang")
mtof = PdObj("mtof")


lfo = PdObj("osc~ 0.1")

osc = PdObj("osc~")
dac = PdObj("dac~")

env = SubPatch("ampenv", simple_env)

env.i1 << trigger.o0
env.i0 << (lfo.o0 + 2) * 200
mtof.i0 << note.o0
osc.i0 << mtof.o0
dac.i0 << osc.o0 * env.o0
seq = ValueSequencer(120, [69, 76, 71, 78], div = 2, value_targets = [note], bang_targets = [trigger])
seq.run()


pd.quit()


