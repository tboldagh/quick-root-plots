#!/usr/bin/env python3.10
from myop import *
options = myop(globals())
options.help=False
options.hist="_NOT_GIVEN_"
options.xtit=None # axes titles
options.ytit=None   
options.drawopt="hp" # see: fast.py draw fuction, this option can be a list, this case options are specified for each hist
options.out=None
options.rmargin=None
options.internal="tr" # add ATLAS internal labels
options.msgsz=0.03


from fast import *

h = get(_file0, options.hist)
style("atlas")
cnv()
if options.rmargin:
    ccnv().SetRightMargin(options.rmargin)
h.Draw(options.drawopt)
if options.xtit:
    h.GetXaxis().SetTitle(options.xtit)
if options.ytit:
    h.GetYaxis().SetTitle(options.ytit)

if isinstance(options.internal, str):
    xbl, ybl, xtr, ytr = posKey2Abs(options.internal)
    options.internal = (xbl, ytr)
if options.internal:
    args = (options.internal) +("#font[72]{ATLAS} #font[42]{Internal}", options.msgsz)
    putlabel(*args)
ccnv().Update()

if options.out:
    save(options.out)

