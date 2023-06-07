#!/usr/bin/env python3.10
from myop import *
options = myop(globals())

options.hist="h_FCalET"
options.drawopt="root: he"
options.logx=0
options.logy=0
options.ylog=options.logy
options.zlog=0
options.xtit=None
options.ytit=None
options.xlabel=None # either true, then labels are copied from source 1 input histogram or list of labels
options.prof=False
options.projy=False
options.line=None
options.fit=False
options.xrange=None
options.yrange=None
options.zrange=None
options.fitrange=None
options.linfitprof=False
options.rebin2D=None
options.wscale=None
options.escale=None # events scale
options.pscale=None # scale to the same number of entries in position
options.lscale=None
options.msg=[]
options.msgpos=(0.6, 0.89)
options.msgsz=0.03
options.out=None
options.rebin=None
options.layout=None
options.legend=[""]
options.legendpos="tr"
options.ratioto=None # either the name or index from 0
options.ratiorange=(0.45,1.55)
options.ratiotit="Ratio"

options.internal=None

from fast import *

style("atlas")

assert _file0, "the root file can not be open"
hists = []
if isinstance(options.hist, str):
    options.hist = [options.hist]
    if not options.out:
        options.out = options.hist[0]

assert options.out, "out option has to be specified"
assert len(_files) == 1 or len(_files) == len(options.hist) or len(options.hist) == 1, "Either single file is supported, or number of files needs to be the same as number of histograms"
if len(_files) == 1: # one input file, all hostograms read from it
    for hname in options.hist:
        h = _file0.Get(hname)
        assert h, "Historgam " +hname+ " does not exist"
        print("Histogram ", h.GetName()) #, " entries ", h.GetEntries()
        hists.append(h)

elif len(_files) == len(options.hist): # same number of inputs as histograms
    for hname, file in zip(options.hist, _files):
        h = file.Get(hname)
        assert h, "Historgam " +hname+ " does not exist"
        print("Histogram ", h.GetName(), " read from ", file.GetName()) #, " entries ", h.GetEntries()
        hists.append(h)

elif len(options.hist) == 1:
    for file in _files:
        h = file.Get(options.hist[0])
        assert h, "Historgam " +options.hist[0]+ " does not exist"
        print("Histogram ", h.GetName(), " read from ", file.GetName()) #, " entries ", h.GetEntries()
        hists.append(h)

assert len(hists) == len(options.legend), "Wrong number of legend elements {} vs {}".format([h.GetName() for h in hists], options.legend)

if isinstance(options.drawopt, str):
    options.drawopt = [options.drawopt]*len(hists)
else:
    assert len(hists) == len(options.drawopt), "Number of drawing options must match number of histograms"

if isinstance(options.msgpos, str):
    xbl, ybl, xtr, ytr = posKey2Abs(options.msgpos)
    options.msgpos = (xbl, ytr)

if isinstance(options.internal, str):
    xbl, ybl, xtr, ytr = posKey2Abs(options.internal)
    options.internal = (xbl, ytr)

if not options.layout:
    options.layout = '2d' if "TH2" in hists[0].ClassName() else None


if options.projy:
    [ h.ProjectionY() for h in hists ]

if options.rebin:
    [ h.Rebin(options.rebin) for h in hists ]

if options.wscale:
    [ h.Scale(1, "width") for h in hists ]

if options.escale:
    [ h.Scale(1./h.GetEntries(), "width") for h in hists ]

if options.pscale != None:
    [ h.Scale(1./h.GetBinContent(h.FindBin( options.pscale ) ), "width") for h in hists ]


if options.rebin2D:
    [ h.Rebin2D(options.rebin2D[0], options.rebin2D[1])  for h in hists ]


ROOT.gStyle.SetPalette(1)
if not options.xrange:
    options.xrange = (10, hists[0].GetXaxis().GetXmin(), hists[0].GetXaxis().GetXmax())
    print("Extracted xrange from the first histogram", options.xrange)
yr = options.yrange
if not options.yrange:
    if "TH1" in hists[0].ClassName():
        options.yrange = (10, hists[0].GetMinimum(), hists[0].GetMaximum()* (1.2 if options.ylog else 10) )
    if "TH2" in hists[0].ClassName():
        options.yrange = (10, hists[0].GetYaxis().GetXmin(), hists[0].GetYaxis().GetXmax())
assert options.xrange, "X range not specified"
assert options.yrange, "Y range not specified"

if not options.ratioto is None:
    cnv(y=600)
    csplit(0.3)
    ccnv(1).SetLogy(options.ylog)
else:
    cnv()
    ccnv(0).SetLogy(options.ylog)

fr = frame(options.xrange, options.yrange)
if options.zrange:
    fr.GetZaxis().SetRangeUser(options.zrange[1], options.zrange[2])

if options.xlabel:
    if isinstance(options.xlabel, list):
        assert fr.GetXaxis().GetNbins() == len(options.xlabel), 'Labels list for xaxis need to have the same length the number of frame bins'
        labs = options.xlabel
    else:
        assert abs(fr.GetXaxis().GetBinWidth(1) -  hists[0].GetXaxis().GetBinWidth(1)) < 0.001, 'Frame histogram has different bin width {} than plotted hist {} this is not allowed for labeled hists'.format(fr.GetXaxis().GetBinWidth(1), hists[0].GetXaxis().GetBinWidth(1))
        labs = [ hists[0].GetXaxis().GetBinLabel(b) for b in range(1, hists[0].GetXaxis().GetNbins()+1) ]
    for bin, lab in zip( range(1, fr.GetXaxis().GetNbins()+1), labs ):
        fr.GetXaxis().SetBinLabel(bin, lab)

if len(hists) > 1:
    legend(options.legendpos)

if not options.xtit:
    options.xtit = hists[0].GetXaxis().GetTitle()
if not options.ytit:
    options.ytit = hists[0].GetYaxis().GetTitle()

axis(options.xtit,  options.ytit )
if options.logx:
    ccnv().SetLogx(1)


if options.zlog:
    ccnv().SetLogz(1)

for h, label, opt in zip(hists, options.legend, options.drawopt):
    # h.SetLineColor(att[0])
    # h.SetMarkerStyle(att[1])
    # h.SetMarkerColor(att[0])
    print(("Drawing histogram {} with label {}".format(h.GetName(), label)))
    draw(h, label, opt=opt)

if options.zlog or options.zrange:
    ccnv().SetLeftMargin(0.15)
    fr.GetYaxis().SetTitleOffset(1.0)


if options.prof:
    prof = h.ProfileX()
    prof.Draw("same e")
    if options.linfitprof:
        prof.Fit("pol1", "", "same")

if options.line:
    for h in hists:
        if options.fitrange:
            f = ROOT.TF1('line'+h.GetName(),options.line, options.fitrange[0], options.fitrange[1])
        else:
            f = ROOT.TF1('line'+h.GetName(),str(options.line), cframe().GetXaxis().GetXmin(), cframe().GetXaxis().GetXmax())
        if options.fit:
            h.Fit(f, "R")
        f.Draw("same")
        f.SetLineColor(h.GetLineColor())

if options.internal:
    args = (options.internal) +("#font[72]{ATLAS} #font[42]{Internal}", options.msgsz)
    putlabel(*args)

texts = []
for index,m in enumerate(options.msg,1):
    if isinstance(m, tuple):
        texts.append( putlabel(*m) )
    else:
        texts.append( putlabel(options.msgpos[0], options.msgpos[1]-(options.msgsz+0.01)*index, m, options.msgsz) )


if options.ratioto:
    if isinstance( options.ratioto, int):
        denominator = [hists[options.ratioto]]
        numerators = [ h for i,h in enumerate(hists) if i != options.ratioto ]
    else:
        denominator = [h for h in hists if h.GetName() == options.ratioto]
        numerators = [h for h in hists if h.GetName() != options.ratioto]
    assert len(denominator) == 1, f"Missing histogram in denominator {options.ratioto}"
    denominator = denominator[0]
    if denominator.ClassName() == "TProfile":
        denominator = denominator.ProjectionX()
    print("ratios of ",  [n.GetName() for n in numerators], "to", denominator.GetName() )
    ccnv(2)
    f = frame(options.xrange, (3,)+options.ratiorange)
    x = f.GetXaxis()
    x.SetTitleSize(0.14)
    x.SetTitleOffset(1.1)
    x.SetLabelSize(0.14)

    y = f.GetYaxis()
    y.SetTitleSize(0.14)
    y.SetTitleOffset(0.55)
    y.SetLabelSize(0.14)
    y.SetNdivisions(6,4,0,True)
    styleOffset(0)
    for n in numerators:
        if n.ClassName() == "TProfile":
            c = n.ProjectionX()
        else:
            c = n.Clone(n.GetName()+"Ratio")
        c.Divide(n, denominator, 1.0, 1.0, "B")
        draw(c, "SKIP", opt="pe")
#        c.Draw("same")

    axis(options.xtit, options.ratiotit)
    one = ROOT.TF1("one", "pol0", options.xrange[1], options.xrange[2])
    one.SetParameter(0, 1)
    one.SetLineWidth(1)
    one.SetLineStyle(ROOT.kDashed)
    one.SetLineColor(ROOT.kBlack)

    one.Draw("Same")





save(options.out)
print("after manual modification s() can save again, s(other) can save with 'other' name")
def s(name=options.out):
    """ for saving again """
    save(name)
