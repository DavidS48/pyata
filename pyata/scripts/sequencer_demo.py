
from sands.pd_obj import PdObj, PdNum, PdMess, SubPatch
from sands.Pd import Pd
from sands.sequencer import ValueSequencer
from sands.abstractions import simple_env

pd = Pd()
pd.init()

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


