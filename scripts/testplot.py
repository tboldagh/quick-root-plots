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
frame((5, -0.1, 1.1), (6, 0, 0.5*options.nsamples))
legend("tr,USl") # move it several times up (U) and shorten (S), and then move to left a bit (l)

axis("Size [mm]", "Occurrences")
draw(hx,"Data X (Poisson)", "hpe")
draw(hy, "Data Y (Binomial)", "he")

label(0.2, 0.90, "Samples comparison", 0.05 )

label(0.75, 0.96, "piROOT", 0.05 )

save("testplot")

