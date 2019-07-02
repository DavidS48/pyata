from sands.pd_obj import PdObj, PdMess, PdInlet, PdMInlet, PdOutlet

def simple_env():
    dec_in = PdInlet()
    trigger = PdMInlet()
    delay = PdObj("delay 20")
    att = PdMess("1 20")
    dec_inst = PdObj("snapshot~")
    dec = PdObj("pack 0 400")
    line = PdObj("line")
    out = PdOutlet()
    att.i0 << trigger.o0
    delay.i0 << trigger.o0
    dec_inst.i0 << dec_in.o0
    dec_inst.i0 << delay.o0
    dec.i1 << dec_inst.o0
    dec.i0 << delay.o0
    line.i0 << att.o0
    line.i0 << dec.o0
    out.i0 << line.o0


