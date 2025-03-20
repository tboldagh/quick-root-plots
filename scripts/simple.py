#!/usr/bin/env python3.10
from myop import *
options = myop(globals())
options.help=False
options.hist="_NOT_GIVEN_"
options.xtit=None # axes titles
options.ytit=None   
options.yrange=None   

options.drawopt="hp" # see: fast.py draw fuction, this option can be a list, this case options are specified for each hist
options.out=None
options.rmargin=None
options.internal="tr" # add ATLAS internal labels
options.msgsz=0.03
options.msg=[] # additional messages
options.msgpos=(0.6, 0.89)



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

if isinstance(options.msgpos, str):
    xbl, ybl, xtr, ytr = posKey2Abs(options.msgpos)
    options.msgpos = (xbl, ytr)

texts = []
for index,m in enumerate(options.msg,1):
    if isinstance(m, tuple):
        texts.append( putlabel(*m) )
    else:
        texts.append( putlabel(options.msgpos[0], options.msgpos[1]-(options.msgsz+0.01)*index, m, options.msgsz) )

if options.yrange:
    h.GetYaxis().SetRangeUser(options.yrange[1], options.yrange[2])
ccnv().Modified()
ccnv().Update()


if options.out:
    save(options.out)

