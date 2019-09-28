from sands.pd_obj import PdObj, PdMess, PdInlet, PdMInlet, PdOutlet, PdNum, SubPatch

def modded_env():
    trigger = PdMInlet()
    dec_in = PdInlet()
    delay = PdObj("delay 20")
    att = PdMess("1 20")
    dec = PdObj("pack 0 400")
    line = PdObj("line")
    out = PdOutlet()
    att.i0 << trigger.o0
    delay.i0 << trigger.o0
    dec.i0 << delay.o0
    line.i0 << att.o0
    line.i0 << dec.o0
    out.i0 << line.o0


def simple_env():
    trigger = PdMInlet()
    delay = PdObj("delay 20")
    att_mess = PdMess("1 20")
    dec_val = PdNum(400)
    dec_mess = PdObj("pack 0 400")
    line = PdObj("line")
    out = PdOutlet()
    att_mess.i0 << trigger.o0
    delay.i0 << trigger.o0
    dec_mess.i0 << delay.o0
    dec_mess.i1 << dec_val.o0
    line.i0 << att_mess.o0
    line.i0 << dec_mess.o0
    out.i0 << line.o0
    return {"decay" : dec_val}

def ping():
    note_in = PdMInlet()
    mtof = PdObj("mtof")
    osc = PdObj("osc~")
    env = SubPatch("ping_env", simple_env)
    out = PdOutlet()
    mtof.i0 << note_in.o0
    osc.i0 << mtof.o0
    env.i0 << note_in.o0
    out.i0 << osc.o0 * env.o0
    return {"decay" : (env, "decay")}

def kick():
    trigger = PdMInlet()
    bang = PdMess("bang")
    pitch_base = PdNum(30)
    pitch_amt = PdNum(30)
    pitch_env = SubPatch("pitch_env", simple_env)
    amp_env = SubPatch("amp_env", simple_env)
    osc = PdObj("osc~ 30")
    out = PdOutlet()
    bang.i0 << trigger.o0
    pitch_env.i0 << bang.o0
    amp_env.i0 << bang.o0
    osc.i0 << pitch_env.o0 * pitch_amt.o0 + pitch_base.o0
    out.i0 << osc.o0 * amp_env.o0

    return {"pitch" : pitch_base,
            "pitch_env" : pitch_amt,
            "pitch_decay" : (pitch_env, "decay"),
            "amp_decay" : (amp_env, "decay")}
    
