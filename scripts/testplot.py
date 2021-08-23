# example fast plot
# can see the result of this script by piroot testplot.py -p "nsamples=100"

from fast import *

from myop import myop
options = myop(globals())
options.nsamples=1000

import ROOT
hx = ROOT.TH1F("x", "My data X", 10, 0, 1)
hy = ROOT.TH1F("y", "My data Y", 10, 0, 1)

rng = ROOT.TRandom()
for i in range(options.nsamples):
    hx.Fill(rng.Poisson(1.2)/10.)
    hy.Fill(rng.Binomial(10, 0.5)/10.)

style("atlas") #try also atlas experiment style
cnv()
frame((5, -0.3, 1.1), (6, 0.1, 0.49*options.nsamples))
legend("tr,uSLww") # move it several times up (u) and shorten (S), and then move to left (L) and make it 2 quants wider

axis("Size [mm]", "Occurrences in an interval of width 0.1")
draw(hx,"Data X (Poisson)", "hpe")
draw(hy, "Data Y (Binomial)", "he")

putlabel("tl,ddLL", "Samples comparison", 0.05 ) # keyed position 

putlabel(0.79, 0.96, "#piR#lower[0.3]{#scale[2]{#bullet}}#kern[-2.5]{#lower[0.2]{#scale[1.4]{#/}}}#kern[0.3]{OT}", 0.05 ) # absoluteposition

move("xlab", "d")
move("xtit", "u")
# the Y axis labeling will be made a bit crazy because the Y title is long
move("ylab", "RR")
move("ytit", "Rrr") # move it left
move("yl", "Lll")
move("yr", "r")
move("xb", "d")
move("xt", "d")

save("testplot")

