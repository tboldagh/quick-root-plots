from myop import *
options = myop(globals())

options.hist="h_FCalET"
options.drawopt="he"
options.logx=0
options.logy=0
options.ylog=options.logy
options.zlog=0
options.xtit=None
options.ytit=None
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
options.ratioto=None
options.ratiorange=(0.45,1.55)
options.internal=None

from fast import *

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
xr = options.xrange if options.xrange else (10, hists[0].GetXaxis().GetXmin(), hists[0].GetXaxis().GetXmax())
yr = options.yrange
if "TH1" in hists[0].ClassName():
    yr = options.yrange if options.yrange else (10, hists[0].GetMinimum(), hists[0].GetMaximum()* (1.2 if options.ylog else 10) )
if "TH2" in hists[0].ClassName():
    yr = options.yrange if options.yrange else (10, hists[0].GetYaxis().GetXmin(), hists[0].GetYaxis().GetXmax())
assert xr, "X range not specified"
assert yr, "Y range not specified"

print(xr, yr)
if options.ratioto:
    cnv(y=600)
    csplit(0.3)
    ccnv(1).SetLogy(options.ylog)
else:
    cnv()
    ccnv(0).SetLogy(options.ylog)

fr = frame(xr, yr)
if options.zrange:
    fr.GetZaxis().SetRangeUser(options.zrange[1], options.zrange[2])
legend(options.legendpos)

axis(options.xtit if options.xtit else hists[0].GetXaxis().GetTitle(), options.ytit if options.ytit else hists[0].GetYaxis().GetTitle())
if options.logx:
    ccnv().SetLogx(1)


if options.zlog:
    ccnv().SetLogz(1)


for h, label in zip(hists, options.legend):
    # h.SetLineColor(att[0])
    # h.SetMarkerStyle(att[1])
    # h.SetMarkerColor(att[0])
    print(("Drawing histogram {} with label {}".format(h.GetName(), label)))
    draw(h, label, opt=options.drawopt)

if options.zlog or options.zrange:
    ccnv().SetLeftMargin(0.15)
    fr.GetYaxis().SetTitleOffset(1.0)
    if "z" in options.drawopt:
        ccnv().SetRightMargin(0.15)
        # palette = hists[0].GetListOfFunctions().FindObject("palette")
        # palette.SetX1NDC(0.88)
        # palette.SetX2NDC(0.93)


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
    args = (options.internal) +("ATLAS #font[42]Internal", options.msgsz)
    label(args)
texts = []
for index,m in enumerate(options.msg,1):
    if isinstance(m, tuple):
        texts.append( Label(*m) )
    else:
        texts.append( Label(options.msgpos[0], options.msgpos[1]-(options.msgsz+0.01)*index, m, options.msgsz) )


if options.ratioto:
    denominator = [h for h in hists if h.GetName() == options.ratioto]
    numerators = [h for h in hists if h.GetName() != options.ratioto]
    assert len(denominator) == 1, "Missing histogram in denominator"+options.ratioto
    denominator = denominator[0]
    print("ok ", denominator.GetName() )
    ccnv(2)
    f = frame(options.xrange, (3,)+options.ratiorange)
    x = f.GetXaxis()
    x.SetTitleSize(0.14)
    x.SetTitleOffset(1.1)
    x.SetLabelSize(0.14)

    y = f.GetYaxis()
    y.SetTitleSize(0.14)
    y.SetTitleOffset(0.75)
    y.SetLabelSize(0.14)
    y.SetNdivisions(6,4,0,True)

    for n in numerators:
        c = n.Clone(n.GetName()+"Ratio")
        c.Divide(n, denominator, 1.0, 1.0, "B")
        c.Draw("same")

    axis(options.xtit, "Ratio")
    one = ROOT.TF1("one", "pol0", options.xrange[1], options.xrange[2])
    one.SetParameter(0, 1)
    one.SetLineWidth(1)
    one.Draw("Same")



    
save(options.out)
print("after manual modification s() can save again, s(other) can save with 'other' name")
def s(name=options.out):
    """ for saving again """
    save(name)
