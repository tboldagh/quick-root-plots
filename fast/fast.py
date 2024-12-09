#from bootstrap import *

import ROOT

_hists=[]
_frames=[]
_legend=None
_legendpos="tr"
_cnvs=[]
_styleOffset=-1

attrsDefault = [(ROOT.kGray+3, ROOT.kFullCircle),
       (ROOT.kOrange-7, ROOT.kFullSquare),
       (ROOT.kSpring+4, ROOT.kFullCircle),
       (ROOT.kRed-3, ROOT.kOpenTriangleDown),
       (ROOT.kBlue-6, ROOT.kOpenTriangleUp),
       (ROOT.kMagenta+1, ROOT.kOpenSquare),
       (ROOT.kOrange+5, ROOT.kOpenCircle),
       (ROOT.kTeal+3, ROOT.kOpenDiamond),
       (ROOT.kRed+2, ROOT.kOpenCross),
       (ROOT.kOrange-3, ROOT.kOpenCircle),
       (ROOT.kTeal-3, ROOT.kOpenSquare),

    ]
attrs = attrsDefault

attrsHollow = [(ROOT.kGray+3, ROOT.kOpenCircle),
       (ROOT.kOrange-7, ROOT.kOpenSquare),
       (ROOT.kSpring+4, ROOT.kOpenDiamond),
       (ROOT.kRed-3, ROOT.kOpenTriangleDown),
       (ROOT.kBlue-6, ROOT.kOpenTriangleUp),
       (ROOT.kMagenta+1, ROOT.kOpenStar),
    ]

def few():
    """change styling for the case of very few (up to 3) plots to have higher contrast"""
    global attrs
    attrs = [(ROOT.kBlack, ROOT.kOpenCircle),
           (ROOT.kRed, ROOT.kOpenSquare),
           (ROOT.kBlue, ROOT.kOpenDiamond)]



def polySet(which="default"):
    """Select which set of polymarkers & colors to use"""
    if which == "default":
        attrs = attrsDefault
    if which == "hollow":
        attrs = attrsHollow



pos = {"tr"  : (0.60, 0.60, 0.92, 0.9),
        "trn" : (0.80, 0.60, 0.92, 0.9),
        "tl"  : (0.22, 0.60, 0.52, 0.9),
        "tc"  : (0.40, 0.60, 0.70, 0.9),
        "br" : (0.60, 0.22, 0.92, 0.42),
        "brn" : (0.80, 0.22, 0.92, 0.42),
        "bc" : (0.40, 0.22, 0.72, 0.42),
        "bl" : (0.20, 0.22, 0.52, 0.42),
        "cc" : (0.45, 0.46, 0.68, 0.68)

}

def moveDirectives(directives, init=(0,0,0,0)):
    moves = {"u": (0, 0.02, 0, 0.02),
            "U": (0, 0.06, 0, 0.06),
            "d": (0, -0.02, 0, -0.02),
            "D": (0, -0.06, 0, -0.06),
            "r": (0.02, 0, 0.02, 0),
            "R": (0.06, 0, 0.06, 0),
            "l": (-0.02, 0, -0.02, 0) ,
            "L": (-0.06, 0, -0.06, 0),
            "n": (0.02, 0, -0.02, 0),
            "N": (0.06, 0, -0.06, 0),
            "w": (-0.02, 0, 0.02, 0),
            "W": (-0.06, 0, 0.06, 0),
            "s": (0, 0.02, 0, -0.02),
            "S": (0, 0.06, 0, -0.06),
            "t": (0, -0.02, 0, 0.02),
            "T": (0, -0.06, 0, 0.06)
    }
    pos=init
    for d in directives:
        assert d in moves, "move directive not known"
        pos = tuple([ c+m for c,m in zip( pos, moves[d]) ])
    return pos


def posKey2Abs(posKey):
    if all( [ k not in posKey for k in pos.keys()] ):
        raise Exception("No legend position "+str(posKey)+ " there are possible: " +" ".join(list(pos.keys()) ))
    directives=posKey.split(",")
    coord = pos[directives[0]]

    if len(directives) == 2:
        coord = moveDirectives(directives[1], coord)
    return coord


def move(what, posKey):
    """Moves plot elements according to the moves key  UDLR (instead of the key a number can be also given)
        Not all move operations work for all elements
    """
    pos = moveDirectives(posKey) if isinstance(posKey, str) else (posKey, posKey, posKey, posKey)
    print ("... Moving", what, pos)
    if what == 'xlab':
        cframe().GetXaxis().SetLabelOffset( cframe().GetXaxis().GetLabelOffset()-pos[1] )

    elif what == 'xtit':
        cframe().GetXaxis().SetTitleOffset( cframe().GetXaxis().GetTitleOffset()-pos[1]*10 )

    elif what == 'ylab':
        cframe().GetYaxis().SetLabelOffset( cframe().GetYaxis().GetLabelOffset()-pos[0] )

    elif what == 'ytit':
        cframe().GetYaxis().SetTitleOffset( cframe().GetYaxis().GetTitleOffset()-pos[0]*10 )

    elif what == 'yl':
        ccnv().SetLeftMargin( ccnv().GetLeftMargin()+pos[0])
    elif what == 'yr':
        ccnv().SetRightMargin( ccnv().GetRightMargin()-pos[0])
    elif what == 'xb':
        ccnv().SetBottomMargin( ccnv().GetBottomMargin()+pos[1])
    elif what == 'xt':
        ccnv().SetTopMargin( ccnv().GetTopMargin()-pos[1])

    else:
        assert False, "Do not know what to move {}".format(what)



def setattrs(newattrs):
    global attrs
    attrs = newattrs

def styleOffset(n = 0):
    global _styleOffset
    _styleOffset = n

def clear():
    print("clearing drawing history")
    global _hists
    global _legend
    global _legendpos
    global _cnvs
    global _styleOffset
    _hists=[]
    _legend=None
    _legendpos="tr"
    _cnvs=[]
    _styleOffset=0


def get(src, name, default_if_missing=None):
    """ Get the object from the file, if missing raises an exception unless  the third argument is provided (that is specimen)"""
    needClosing = False
    if isinstance(src, str): # this is likely file name, so needs to be opened
        needClosing = True
        src = ROOT.TFile.Open(src, "OLD")
    o = src.Get(name)
    if not o:
        if not default_if_missing:
            assert o, "Object of name "+ name +" absent in the file: "+src.GetName()
        o = default_if_missing(name)
    if needClosing:
        src.Close()
    return o

def style(name="atlas"):
    """Apply a predefined style, ATLAS experiment one and a compact are the only styles available"""
    def _atlas():
        """Make style like ATLAS experiment"""
        ROOT.gStyle.SetPadTopMargin(0.05)
        ROOT.gStyle.SetPadRightMargin(0.05)
        ROOT.gStyle.SetPadBottomMargin(0.16)
        ROOT.gStyle.SetPadLeftMargin(0.16)
        ROOT.gStyle.SetLegendBorderSize(0)
        ROOT.gStyle.SetLegendFillColor(0)
        ROOT.gStyle.SetTitleXOffset(1.4)
        ROOT.gStyle.SetTitleYOffset(1.4)
        font = 42 # Helevetica
        ROOT.gStyle.SetTextFont(font)
        ROOT.gStyle.SetLabelFont(font,"x")
        ROOT.gStyle.SetTitleFont(font,"x")
        ROOT.gStyle.SetLabelFont(font,"y")
        ROOT.gStyle.SetTitleFont(font,"y")
        ROOT.gStyle.SetLabelFont(font,"z")
        ROOT.gStyle.SetTitleFont(font,"z")
        tsize = 0.05
        ROOT.gStyle.SetTextSize(tsize)
        ROOT.gStyle.SetLabelSize(tsize,"x")
        ROOT.gStyle.SetTitleSize(tsize,"x")
        ROOT.gStyle.SetLabelSize(tsize,"y")
        ROOT.gStyle.SetTitleSize(tsize,"y")
        ROOT.gStyle.SetLabelSize(tsize,"z")
        ROOT.gStyle.SetTitleSize(tsize,"z")

        # use bold lines and markers
        ROOT.gStyle.SetMarkerStyle(20)
        ROOT.gStyle.SetMarkerSize(0.8)
        ROOT.gStyle.SetHistLineWidth(2)
        ROOT.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes
        ROOT.gStyle.SetGridColor(ROOT.kGray)
        ROOT.gStyle.SetGridWidth(1)
        ROOT.gStyle.SetGridStyle(ROOT.kSolid)
        # get rid of X error bars
        #ROOT.gStyle.SetErrorX(0.001)
        # get rid of error bar caps
        ROOT.gStyle.SetEndErrorSize(0.)
        # do not display any of the standard histogram decorations
        ROOT.gStyle.SetOptTitle(0)
        #ROOT.gStyle.SetOptStat(1111)
        ROOT.gStyle.SetOptStat(0)
        #ROOT.gStyle.SetOptFit(1111)
        ROOT.gStyle.SetOptFit(0)
        # put tick marks on top and RHS of plots
        ROOT.gStyle.SetPadTickX(1)
        ROOT.gStyle.SetPadTickY(1)
        #/ my tunnings
        ROOT.gStyle.SetOptStat("")
        ROOT.gStyle.SetPadGridY(0)
        ROOT.gStyle.SetPadGridX(0)
        ROOT.gStyle.SetStatFontSize(0.1)
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetStatStyle(0)
        ROOT.gStyle.SetMarkerSize(0.8)
        ROOT.gStyle.SetMarkerStyle(ROOT.kOpenCircle)
        ROOT.gStyle.SetMarkerColor(ROOT.kBlue)
        #  ROOT.gStyle.SetStatX(0.36)
        ROOT.gStyle.SetStatW(0.45)
        ROOT.gStyle.SetStatFormat("4.0g")
        # ROOT.TGaxis.SetMaxDigits(2)
        # ROOT.TGaxis.SetExponentOffset(-0.2, -0.1, "y") # X and Y offset for Y axis
        # ROOT.TGaxis.SetExponentOffset(0.05, 0.01, "x")

        ROOT.gROOT.ForceStyle()
    if name == "atlas":
        _atlas()
    elif name == "compact":
        _atlas()
        ROOT.gStyle.SetPadTopMargin(0.02)
        ROOT.gStyle.SetPadRightMargin(0.02)
        ROOT.gStyle.SetPadBottomMargin(0.08)
        ROOT.gStyle.SetPadLeftMargin(0.05)
        ROOT.gStyle.SetTitleOffset(1.2, "X")
        ROOT.gStyle.SetTitleOffset(1.2, "Y")
        ROOT.gROOT.ForceStyle()





def cnv(name=None, x=500, y=500):
    """Create canvas of aforementioned sizes"""
    global _cnvs
    name =  "cnv%d" % len(_cnvs) if not name else name
    c = ROOT.TCanvas(name, name, x, y)
    _cnvs.append(c)
    return c
# cnv()

def csplit(factor=0.4):
    ccnv().SetLeftMargin(0.0)
    ccnv().Divide(1, 2, 0.01)
    top = ccnv().cd(1)
    top.SetPad(0, factor , 1, 1)
    top.SetBottomMargin(0.01)
    top.SetTopMargin(0.07)
    top.SetLeftMargin(0.17)
    bottom = ccnv().cd(2)
    bottom.SetPad(0, 0. , 1, factor)
    bottom.SetLeftMargin(0.17)
    bottom.SetBottomMargin(0.35)

def ccnv(pad=0):
    """Current canvas"""
    global _cnvs
    if pad == 0:
        return _cnvs[-1]
    _cnvs[-1].cd(pad)
    return _cnvs[0].GetPad(pad)

def new():
    """Prepare for a new plot in one scipt"""
    global _hists
    _hists = []
    global _legend
    _legend = None
    styleOffset( )
    return cnv()


def frame(xr, yr=(1,0,1)):
    """ Make frame (axes), arguments are divisions & ranges for each axis packed in 2 element tuple
        e.g. (10, -1,1) means many divisions and range from -1 to 1
    """
    global _frames
    global _cnvs
    f = ROOT.TH2C("frame%d%d" % (len(_cnvs),_cnvs[0].GetNumber()), "frame", xr[0], xr[1], xr[2], yr[0], yr[1], yr[2])
    f.Draw()
#    f.GetXaxis().SetTitleOffset(1.2)
    f.GetXaxis().SetNdivisions(xr[0] + 100*5)
    f.GetXaxis().SetMaxDigits(3)
#    f.GetYaxis().SetTitleOffset(2)
    f.GetYaxis().SetNdivisions(yr[0] + 100*5)
    f.GetYaxis().SetMaxDigits(3)
    _frames.append(f)
    return f

def cframe():
    """Current flame"""
    global _frames
    if len(_frames[0]) ==  0:
        raise Exception("cframe: No frame histogram defined yet")
    return _frames[-1]

def _getLegend():
    global _legend
    if not _legend:
        posNDC=tuple( i*0.01 for i in (70, 50, 92, 77) )
        _legend = ROOT.TLegend( *posNDC )
    return _legend


def __decode_color(spec):
    for k in ["kGray", "kOrange", "kSpring",
                "kRed", "kBlue", "kMagenta",
                "kOrange", "kTeal", "kRed", "kOrange", "kGreen"]:
        if k in spec:
            return eval(f"ROOT.{k}")
    return 0

def __decode_marker(spec):
    for m in ["kFullCircle", "kFullSquare",
                    "kFullCircle",  "kOpenTriangleDown", "kOpenTriangleUp",
                    "kOpenSquare",  "kOpenCircle",  "kOpenDiamond", "kOpenCross",
                    "kOpenCircle"]:
        if m in spec:
            return eval(f"ROOT.{m}")
    raise Exception(f"{spec} can be decoded as marker")

def draw(h, label="", opt="", legendopt="lp", newData=True):
    """Draw (histogram, graph,...) on current canvas,
       opt - is passed to Draw (modulo the option same)
           - it contains basic ROOT Draw directives but can also explicit color specification
       legendopt - option to present on legend ()
       newData - can be set to false to keep the same style as previously drawn data
       """    
    if label is None:
        label = h.GetName()
    def check_keywords(k):
        if k in opt and not f'{k}:' in opt:
            raise Exception(f"When using {k} option, use syntax: {k}: XYZ not {k} XYZ")
    [check_keywords(k) for k in ['color', 'marker', 'root']]
    ops = opt.split(" ")
    marker = 0
    color = 0
    if 'color:' in ops:
        color = __decode_color(ops[ops.index("color:")+1])

    if 'marker:' in ops:
        marker = __decode_marker(ops[ops.index("marker:")+1])

    if marker == 0 and color == 0:
        global _styleOffset
        if newData:
            _styleOffset += 1
        color = attrs[_styleOffset][0]
        marker = attrs[_styleOffset][1]
    global _hists

    if 'fill' in ops:
        h.SetFillColorAlpha(color, 0.5)
        h.SetFillStyle(1001)
        ops.remove('fill')

    if "root:" in ops:
        ropt = ops[ops.index("root:")+1]
    else:
        ropt = opt
        
    ropt = ropt+" same"
    if 'TF1' in h.ClassName():
        ropt = "l same"


    print(h.GetName(), ropt)
    h.Draw(ropt)
    _hists.append( h )
    if label != "SKIP": # means to add to the legend
        if 'p' not in opt:
            legendopt = legendopt.replace('p', '')
        _getLegend().AddEntry(h, label, legendopt)
    h.SetLineColor(color)

    if 'h' in ropt and 'TGraph' in h.ClassName():
        raise Exception('The h draw option given in: '+ropt+' can not be used for TGraphs or TEfficiency')


    if 'p' in ropt:
        h.SetMarkerColor(color)
        h.SetMarkerStyle(marker)            
    else:
        h.SetMarkerColor(0)
        h.SetMarkerStyle(0)

    if 'TGraphErrors' in h.ClassName() and "2" in ropt:
        h.SetFillStyle(3001)
        h.SetFillColor(color)


def stack(st, h, label=None, tolegend="true"):
    """Plot in a 'stack' style"""
    global _hists
    if tolegend:
        _hists.append( h )
        _getLegend().AddEntry(h, label)
    h.SetFillStyle(1001)
    st.Add(h)

def nhists():
    global _hists
    return len(_hists)

def legend(posKey="tr", title = ""):
    """Add the legend at a position given by the positioning key (see docu)"""
    coord = posKey2Abs(posKey)
    global _legend
    if not _legend:
        _legend = ROOT.TLegend( *coord )

    if title != "":
        _legend.SetHeader(title)

    _legend.Draw("pl")
    return _legend

def axis(x, y):
    """Label axes if the frame was used"""
    global _frames
    assert len(_frames) > 0, "No frames to set axes"
    for h in _frames[::-1]:
        if "frame" in h.GetName():
            h.GetXaxis().SetTitle(x)
            h.GetYaxis().SetTitle(y)
            return

    raise Exception("No histogram named *frame*, axes title not set")


def yopen(factor):
    ymin = _hists[0].GetMinimum()
    ymax = _hists[0].GetMaximum()
    _hists[0].GetYaxis().SetRangeUser(ymin*(1.-factor), ymax*(1.+factor))



def _savePrimitive (obj):
    print("..... saving ", obj.GetName())
    obj.Write()


def _followSubPads(pad, currentdir):
    listOfPrimitives  = pad.GetListOfPrimitives()
    for obj in listOfPrimitives:
        print("..... found ", obj.GetName())

        if obj.InheritsFrom("TPad"):
            subdir = currentdir.mkdir(obj.GetName(), obj.GetTitle())

            print(".... saving in the directory ", gDirectory.GetName())
            _followSubPads( obj, currentdir )

        if obj.InheritsFrom("TH1") or obj.InheritsFrom("TGraph") or obj.InheritsFrom("TEfficiency"):
            _savePrimitive( obj )


def _save(cnv, name, dumpROOT=False, base ="plots"):
    anyformat=False
    if name.endswith(".pdf"):
        anyformat=True
        print(".. saving ", cnv.GetTitle(), " in the file ", name )        
        cnv.SaveAs(name)
    if name.endswith(".png") : # require only specific formats
        anyformat=True
        print(".. saving ", cnv.GetTitle(), " in the file ", name )
        cnv.SaveAs(name)
    if not anyformat:
        print(".. saving ", cnv.GetTitle(), " in the file ", name, "in pdf and png")
        cnv.SaveAs(name+'.pdf')
        cnv.SaveAs(name+'.png')

    if dumpROOT:
        cnv.SaveAs( name + ".root" )
        # take all the graphs and histograms in all the pads and dump them independently
        fname = name + ".pieces.root"
        f = ROOT.TFile.Open( fname, "RECREATE")
        assert f, "File "+ fname + " can no tbe opened"
        print("... Saving pieces to the file ", f.GetName())
        _followSubPads( cnv, f )
        f.Write()
        f.Close()


def _saveToDir( cnv,  dirn,  name, dumpROOT=False):
    print("... Saving to the dir/name: plots" , dirn+"/"+name)
    startdir = ROOT.gSystem.WorkingDirectory()
    changedto = ROOT.gSystem.ChangeDirectory(dirn)
    if not changedto:
        ROOT.gSystem.mkdir(dirn, True)

    ROOT.gSystem.ChangeDirectory(dirn)
    print(".. changed to directory "+dirn)

    _save(cnv, name, dumpROOT, "")
    ROOT.gSystem.ChangeDirectory(startdir)



def save(name, dumpROOT=False):
    """Save the content of current canvas as PDF in plots/ subdir, if dumpROOT is enabled additional ROOT file with all the conntent is made"""
    global _cnvs
    global _legend
    global _legendpos
    ROOT.gStyle.SetOptTitle(0)
    _cnvs[-1].Update()
    _saveToDir(_cnvs[-1], "plots", name, dumpROOT=dumpROOT)

def s(name):
    """A abbreviated save"""
    global _cnvs
    global _legend
    global _legendpos
    _saveToDir(_cnvs[-1], "", name, dumpROOT=False)


def _label(x, y, text, textsize=0.1):
    l = ROOT.TLatex() #l.SetTextAlign(12)
    l.SetTextSize(textsize)
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextColor(ROOT.kBlack)
    return l.DrawLatex(x,y, text)

def logy():
    ccnv().SetLogy(1)


def _putlabelABS(locx, locy, text, sz=0.1):
    if locx < 0:
        locx = 1 + locx
    if locy < 0:
        locy = 1 + locy
    l = ROOT.TLatex(); #l.SetTextAlign(12);
    l.SetTextSize(sz);
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextColor(ROOT.kBlack)
    l.DrawLatex(locx, locy, text)


def putlabel(posXOrKey, posYOrText, textOrFont=None, sz=0.1):
    """Puts label in absolute position or in position given by the key"""
    if isinstance(posXOrKey, str):
        coords=posKey2Abs(posXOrKey)
        print("label pos", coords)
        _putlabelABS(coords[0], coords[-1], posYOrText, textOrFont if textOrFont else sz)
    else:
        _putlabelABS(posXOrKey, posYOrText, textOrFont, sz)


def allbins(hist, xr=None, yr=None, zr=None):
    """Utility aiding iteration over all bins (of N D histograms)"""
    if 'TAxis' in hist.ClassName():
        for b in range(1, hist.GetNbins()+1):
            yield b
    if 'TH1' in hist.ClassName() or 'TProfile' in hist.ClassName():
        for b in xr or range(1, hist.GetXaxis().GetNbins()+1):
            yield b
    if 'TH2' in hist.ClassName():
        for b in xr or range(1, hist.GetXaxis().GetNbins()+1):
            for c in yr or range(1, hist.GetYaxis().GetNbins()+1):
                yield b, c
    if 'TH3' in hist.ClassName():
        for b in xr or range(1, hist.GetXaxis().GetNbins()+1):
            for c in yr or range(1, hist.GetYaxis().GetNbins()+1):
                for d in zr or range(1, hist.GetZaxis().GetNbins()+1):
                    yield b, c, d

# TGraph related functions
def tograph(h):
    """Convert to TGraphErrors if objects is not a TGraph already """
    if "TGraph" in h.ClassName():
        return h
    return ROOT.TGraphErrors(h)

def rebin(h, n):
    """Rebin using root rebinning for plain hists, do custom action for TEfficiency"""
    if "TH1" in h.ClassName() or "TProfile" in h.ClassName():
        h.Rebin(n)
    if "TEfficiency" in h.ClassName():
        num = h.GetPassedHistogram()
        den = h.GetTotalHistogram()
        num.Rebin(n)
        den.Rebin(n)
        h = ROOT.TEfficiency(num, den)

def movex(graph, offset):
    for p in range(graph.GetN()):
        pos = graph.GetPointX(p)
        graph.SetPointX(p, pos+offset)
