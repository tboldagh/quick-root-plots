#!/usr/bin/env python3.10
from myop import *
options = myop(globals())

options.hist="h_FCalET"
options.drawopt="" # see: fast.py draw fuction, this option can be a list, this case options are specified for each hist
options.logx=0
options.logy=0
options.zlog=0
options.xtit=None # axes titles
options.ytit=None
options.xlabel=None # either true, then labels are copied from source 1 input histogram or list of labels
options.prof=False
options.projx=False
options.projy=False
options.profx=False
options.profy=False
options.probins=None
options.line=None
options.fit=False
options.xrange=None # ranges of the plot in x (10, 0, 5) = many ticks (10), in range 0 to 5
options.yrange=None 
options.zrange=None
options.fitrange=None
options.linfitprof=False
options.rebin2D=None
options.wscale=None # just width scale
options.escale=None # events scale
options.pscale=None # scale to the same number of entries in a given position
options.ascale=None # arbitrary scale applied to each histogram
options.msg=[] # additional messages
options.msgpos=(0.6, 0.89)
options.msgsz=0.03
options.out=None # output file name
options.rebin=None # rebining e.g. when set to 2 two bins will be merged
options.layout=None # 2d for 2D hists
options.legend=[""] # names to be put on the legend
options.legendpos="tr" # 
options.ratioto=None # either the name or index from 0
options.ratiorange=(0.45,1.55)
options.ratiotit="Ratio"
options.ratiotype="ratio" # other: diff - plots y - ref, rel - plots (y - ref) / ref, pull - (y - ref)/sigma y
options.ratioscale=None # scale ratio by a value
options.rmargin=None

options.internal=None
options.cd="" # histograms from common path

from fast import *

style("atlas")

assert _file0, "the root file can not be open"
hists = []
if isinstance(options.hist, str):
    options.hist = [options.hist]
    if not options.out:
        options.out = options.hist[0]

# strip hist names from drawing options
options.histdraw = [(h.split(':')[1:]+[""])[0] for h in options.hist]
options.hist = [h.split(':')[0] for h in options.hist]

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
        assert h, "Histogram " +hname+ " does not exist"
        print("Histogram ", h.GetName(), " read from ", file.GetName()) #, " entries ", h.GetEntries()
        hists.append(h)

elif len(options.hist) == 1:
    for file in _files:
        h = file.Get(options.cd+options.hist[0])
        assert h, "Histogram " +options.hist[0]+ " does not exist in " +file.GetPath()
        print("Histogram ", h.GetName(), " read from ", file.GetName()) #, " entries ", h.GetEntries()
        hists.append(h)

if options.legend is not None:
    assert len(hists) == len(options.legend), "Wrong number of legend elements {} vs {}".format([h.GetName() for h in hists], options.legend)

hists = [ h.CreateGraph("e0") if h.ClassName() == "TEfficiency" else h for h in hists ]


if len(hists) <= 3:
    print(".. small number of histograms switching to contrast style")
    few()

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
    if options.probins:
        [ h.GetXaxis().SetRange(*options.probins) for i,h in enumerate(hists) ]
    hists=[ h.ProjectionY(h.GetName()+f"_h{i}") for i,h in enumerate(hists) ]

if options.projx:
    if options.probins:
        [ h.GetYaxis().SetRange(*options.probins) for i,h in enumerate(hists) ]
    hists=[ h.ProjectionX(h.GetName()+f"_h{i}") for i,h in enumerate(hists) ]

if options.profy:
    if options.probins:
        [ h.GetXaxis().SetRange(*options.probins) for i,h in enumerate(hists) ]
    hists=[ h.ProfileY(h.GetName()+f"_h{i}") for i,h in enumerate(hists) ]

if options.profx:
    if options.probins:
        [ h.GetYaxis().SetRange(*options.probins) for i,h in enumerate(hists) ]
    hists=[ h.ProfileX(h.GetName()+f"_h{i}") for i,h in enumerate(hists) ]

if options.rebin:
    [ h.Rebin(options.rebin) for h in hists ]

if options.wscale:
    [ h.Scale(1, "width") for h in hists ]

if options.escale:
    [ h.Scale(1./h.GetSumOfWeights(), "width") for h in hists ]

if options.pscale != None:
    [ h.Scale(1./h.GetBinContent(h.FindBin( options.pscale ) ), "width") for h in hists ]

if options.ascale != None:
    print("... applying scale factors ", options.ascale)
    assert len(options.ascale) == len(hists), "Need the same number of scale factors "+ options.ascale +" as number of hists" + len(hists)
    [ h.Scale(float(s)) for s,h in zip(options.ascale, hists) ]


if options.rebin2D:
    [ h.Rebin2D(options.rebin2D[0], options.rebin2D[1])  for h in hists ]


ROOT.gStyle.SetPalette(1)
if not options.xrange:
    options.xrange = (10, hists[0].GetXaxis().GetXmin(), hists[0].GetXaxis().GetXmax())
    print("Extracted xrange from the first histogram", options.xrange)
yr = options.yrange
if not options.yrange:
    if "TH1" in hists[0].ClassName():
        max_bincount = max(h.GetMaximum() for h in hists)*(10 if bool(options.logy)==True else 1.2)
        min_bincount = min(h.GetMinimum() for h in hists) 
        min_bincount = 10e-3*max_bincount if bool(options.logy)==True else min_bincount
        options.yrange = (10, min_bincount, max_bincount)
    if "TH2" in hists[0].ClassName():
        options.yrange = (10, hists[0].GetYaxis().GetXmin(), hists[0].GetYaxis().GetXmax())
assert options.xrange, "X range not specified"
assert options.yrange, "Y range not specified"

    


if not options.ratioto is None:
    cnv(y=600)
    csplit(0.30)
    ccnv(1).SetLogy(options.logy)
    ccnv(1).SetLogx(options.logx)
    ccnv(2).SetLogx(options.logx)
    ccnv(1) # current pad
else:
    cnv()
    ccnv(0).SetLogy(options.logy)
    ccnv(0).SetLogx(options.logx)
    if options.layout == '2d' or options.layout == '2D':
        ccnv().SetRightMargin(0.15)


if options.rmargin and options.ratioto is None:
    ccnv().SetRightMargin(options.rmargin)

if options.rmargin and options.ratioto:
    ccnv(0).SetRightMargin(options.rmargin)
    ccnv(1).SetRightMargin(options.rmargin)


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

if len(hists) > 1 and options.legend:
    legend(options.legendpos)

if not options.xtit:
    options.xtit = hists[0].GetXaxis().GetTitle()
if not options.ytit:
    options.ytit = hists[0].GetYaxis().GetTitle()

axis(options.xtit,  options.ytit )


if options.zlog:
    ccnv().SetLogz(1)

# drawing histograms
legend_or_nothing = options.legend if options.legend else [""]*len(hists)
for h, label, opt in zip(hists, legend_or_nothing, options.drawopt):
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

if options.legend:
    legend(options.legendpos) # redraw the legend (not clear why needed sometimes)

if options.ratioto != None:
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
    y = fr.GetYaxis()
    y.SetTitleSize(0.06)
    y.SetTitleOffset(1.25)
    y.SetLabelSize(0.06)

    ccnv(2)    
    fb = frame(options.xrange, (3,)+options.ratiorange)
    x = fb.GetXaxis()
    x.SetTitleSize(0.14)
    x.SetTitleOffset(1.2)
    x.SetLabelSize(0.14)

    y = fb.GetYaxis()
    y.SetTitleSize(0.14)
    y.SetTitleOffset(0.55)
    y.SetLabelSize(0.14)
    y.SetNdivisions(6,4,0,True)
    y.SetNoExponent(1)


    def _divHist(dest, numerator, denominator):
        if options.ratiotype == "ratio":
            dest.Divide(numerator, denominator, 1.0, 1.0, "B")
        elif options.ratiotype == "diff":
            dest.Add(denominator, -1.0)
        elif options.ratiotype == "rel":
            dest.Add(numerator, denominator, -1.0)
            dest.Divide(dest, denominator, 1.0, 1.0, "B")
        elif options.ratiotype == "pull":
            uncertainties = [ numerator.GetBinError(b) for b in allbins(n)]
            dest.Add(numerator, denominator, -1.0)            
            for b, u in zip(allbins(c), uncertainties):
                print(b , u)
                dest.SetBinContent(b, dest.GetBinContent(b)/uncertainties[b-1]) if uncertainties[b-1] != 0.0 else dest.SetBinContent(b, 0)
        if options.ratioscale:
            dest.Scale(options.ratioscale)  


    def _divAsymmErrorsGraph(dest, numerator, denominator):
        for p in range(numerator.GetN()):
            x = numerator.GetPointX(p)
            xErrHigh = numerator.GetErrorXhigh(p)
            xErrLow = numerator.GetErrorXlow(p)

            ynum = numerator.GetPointY(p)
            yden = denominator.GetPointY(p)
            if yden == 0 or ynum == 0:
                print(f".... WARNING skipping point {p} in the ratio because either numerator {ynum} or denominator {yden} is zero")
                continue
            yErrNumHigh = numerator.GetErrorYhigh(p)
            yErrNumLow = numerator.GetErrorYlow(p)

            yErrDenHigh = denominator.GetErrorYhigh(p)
            yErrDenLow = denominator.GetErrorYlow(p)
            import math
            sq = lambda x: math.pow(x, 2)
            yErrLow = math.sqrt(sq(ynum/yden)*( sq(yErrNumLow/ynum) + sq(yErrDenLow/yden) ))
            yErrHigh = math.sqrt(sq(ynum/yden)*( sq(yErrNumHigh/ynum) +  sq(yErrDenHigh/yden) ))

            if options.ratiotype == "ratio":
                dest.SetPoint(p, x, ynum/yden)
                dest.SetPointError(p, xErrLow, xErrHigh, yErrLow, yErrHigh)

    styleOffset(0)
    for i, num in enumerate(numerators):
        if num.ClassName() == "TProfile":
            c = num.ProjectionX(f"Ratio{i}")
            _divHist(c, num, denominator)
        elif "TH1" in num.ClassName():
            c = num.Clone(num.GetName()+f"Ratio{i}")
            _divHist(c, num, denominator)
        elif num.ClassName() == "TGraphAsymmErrors":
            c = num.Clone(f"Ratio{i}")
            _divAsymmErrorsGraph(c,num, denominator)
        draw(c, "SKIP", opt="pe")

    axis(options.xtit, options.ratiotit)
    one = ROOT.TF1("one", "pol0", options.xrange[1], options.xrange[2])
    if options.ratiotype == "ratio":
        one.SetParameter(0, 1)
    else:
        one.SetParameter(0, 0)

    one.SetLineWidth(1)
    one.SetLineStyle(ROOT.kDashed)
    one.SetLineColor(ROOT.kBlack)

    one.Draw("Same")



save(options.out)
print("after manual modification s() can save again, s(other) can save with 'other' name")
def s(name=options.out):
    """ for saving again """
    save(name)
