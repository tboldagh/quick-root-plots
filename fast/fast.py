#from bootstrap import *

import ROOT

_hists=[]
_legend=None
_legendpos="tr"
_cnvs=[]
_styleOffset=0
attrs = [(ROOT.kGray+3, ROOT.kFullCircle), 
       (ROOT.kOrange-7, ROOT.kFullSquare),
       (ROOT.kSpring+4, ROOT.kFullCircle),
       (ROOT.kRed-3, ROOT.kOpenTriangleDown),
       (ROOT.kBlue-6, ROOT.kOpenTriangleUp),
       (ROOT.kMagenta+1, ROOT.kOpenSquare),
       (ROOT.kOrange+5, ROOT.kOpenCircle),
       (ROOT.kTeal+3, ROOT.kOpenDiamond),
    ] 

def setattrs(newattrs):
    global attrs
    attrs = newattrs

def styleOffset(n = 0):
    global _styleOffset
    _styleOffset = n
    
def clear():
    print("clearing bffered drawing history")
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
    o = src.Get(name)
    if not o:        
        if not default_if_missing:
            assert o, "Object of name "+ name +" absent in the file: "+src.GetName()
        o = default_if_missing(name)
    return o

def style(name="atlas"):
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
        ROOT.gStyle.SetMarkerStyle(20);
        ROOT.gStyle.SetMarkerSize(0.8);
        #  atlasStyle->SetHistLineWidth(2.);
        ROOT.gStyle.SetHistLineWidth(1);
        ROOT.gStyle.SetLineStyleString(2,"[12 12]"); # postscript dashes
        ROOT.gStyle.SetGridColor(ROOT.kGray);
        ROOT.gStyle.SetGridWidth(1);
        ROOT.gStyle.SetGridStyle(ROOT.kSolid);
        # get rid of X error bars
        #ROOT.gStyle.SetErrorX(0.001);
        # get rid of error bar caps
        ROOT.gStyle.SetEndErrorSize(0.);
        # do not display any of the standard histogram decorations
        #ROOT.gStyle.SetOptTitle(0);
        #ROOT.gStyle.SetOptStat(1111);
        ROOT.gStyle.SetOptStat(0);
        #ROOT.gStyle.SetOptFit(1111);
        ROOT.gStyle.SetOptFit(0);
        # put tick marks on top and RHS of plots
        ROOT.gStyle.SetPadTickX(1);
        ROOT.gStyle.SetPadTickY(1);
        #/ my tunnings
        ROOT.gStyle.SetOptStat("");
        ROOT.gStyle.SetPadGridY(0);
        ROOT.gStyle.SetPadGridX(0);
        ROOT.gStyle.SetStatFontSize(0.1);
        ROOT.gStyle.SetStatBorderSize(0);
        ROOT.gStyle.SetStatStyle(0);
        ROOT.gStyle.SetMarkerSize(0.8);
        ROOT.gStyle.SetMarkerStyle(ROOT.kOpenCircle);
        ROOT.gStyle.SetMarkerColor(ROOT.kBlue);
        #  ROOT.gStyle.SetStatX(0.36);
        ROOT.gStyle.SetStatW(0.45);
        ROOT.gStyle.SetStatFormat("4.0g");
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
    global _cnvs
    name =  "cnv%d" % len(_cnvs) if not name else name
    c = ROOT.TCanvas(name, name, x, y)
#    c.SetLeftMargin(0.2)
    _cnvs.append(c)
    return c
# cnv()        

def csplit(factor=0.4):
    ccnv().SetLeftMargin(0.0)
    ccnv().Divide(1, 2, 0.01)
    top = ccnv().cd(1)
    top.SetPad(0, factor , 1, 1)
    top.SetBottomMargin(0.01)
    top.SetLeftMargin(0.2)
    bottom = ccnv().cd(2)
    bottom.SetPad(0, 0. , 1, factor)
    bottom.SetLeftMargin(0.2)
    bottom.SetBottomMargin(0.35)
    #ccnv().cd(2).SetBackgroundColor(ROOT.kRed)

def ccnv(pad=0):
    global _cnvs
    if pad == 0:
        return _cnvs[-1]
    _cnvs[-1].cd(pad)
    return _cnvs[0].GetPad(pad)

def new():
    global _hists
    _hists = []
    global _legend
    _legend = None
    styleOffset( )
    return cnv()



def frame(xr, yr=(1,0,1)):
    global _hists
    global _cnvs
    f = ROOT.TH2C("frame%d%d" % (len(_cnvs),_cnvs[0].GetNumber()), "frame", xr[0], xr[1], xr[2], yr[0], yr[1], yr[2])
    f.Draw()    
#    f.GetXaxis().SetTitleOffset(1.2)
    f.GetXaxis().SetNdivisions(xr[0] + 100*5)
#    f.GetYaxis().SetTitleOffset(2)
    f.GetYaxis().SetNdivisions(yr[0] + 100*5)
    
    _hists.append(f)
    return f

def cframe():
    global _hists
    if _hists[0].GetTitle() == "frame":
        return _hists[0]
    raise "cframe: No frame histogram defined yet"

def _getLegend():
    global _legend
    if not _legend:
        posNDC=tuple( i*0.01 for i in (70, 50, 92, 77) )
        _legend = ROOT.TLegend( *posNDC )
    return _legend
    

def draw(h, label=None, opt="", tolegend=True, legendopt="lp"):
    if not label:
        label = h.GetName()
    global _hists

    opt =  opt if len(_hists) == 0 else "same "+opt
    h.Draw(opt)
    if tolegend:    
        _hists.append( h )
        _getLegend().AddEntry(h, label, legendopt)
    global _styleOffset
    h.SetLineColor(attrs[_styleOffset][0])
    if 'p' in opt:
        h.SetMarkerColor(attrs[_styleOffset][0])
        h.SetMarkerStyle(attrs[_styleOffset][1])
    _styleOffset += 1


def stack(st, h, label=None, tolegend="true"):
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
    pos = {"tr"  : (0.60, 0.60, 0.92, 0.9),
           "trn" : (0.80, 0.60, 0.92, 0.9),           
           "tl"  : (0.22, 0.60, 0.52, 0.9),
           "tc"  : (0.40, 0.60, 0.70, 0.9),
           "br" : (0.60, 0.22, 0.92, 0.42),           
           "brn" : (0.80, 0.22, 0.92, 0.42),
    }
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

    if all( [ k not in posKey for k in pos.keys()] ):
        raise Exception("No legend position "+posKey+ " there are possible: " +" ".join(list(pos.keys()) ))
    global _legend
    directives=posKey.split(",")
    coord = pos[directives[0]]

    if len(directives) == 2:
        for d in directives[1]:
            assert d in moves, "Legend move directive not known"
            print( moves[d])
            coord = tuple([ c+m for c,m in zip( coord, moves[d]) ])

    if not _legend:
        _legend = ROOT.TLegend( *coord )

    if title != "":
        _legend.SetHeader(title)
        
    _legend.Draw("pl")
    return _legend
    
def axis(x, y):
    global _hists
    assert len(_hists) > 0, "No histograms to set axes"
    for h in _hists[::-1]:
        if "frame" in h.GetName():
            h.GetXaxis().SetTitle(x)
            h.GetYaxis().SetTitle(y)
            return
        
    raise "No histogram named *frame*, axes title not set"
            

def yopen(factor):
    ymin = _hists[0].GetMinimum()
    ymax = _hists[0].GetMaximum()
    _hists[0].GetYaxis().SetRangeUser(ymin*(1.-factor), ymax*(1.+factor))



def _savePrimitive (obj):
    print("..... saving ", obj.GetName()) 
    obj.Write();  


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
    print(".. saving ", cnv.GetTitle(), " in the file ", name+".pdf")
    cnv.SaveAs(name+".pdf")
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
    print("... Saving to the dir/name: plots" , dirn , "/" , name)
    startdir = ROOT.gSystem.WorkingDirectory()
    changedto = ROOT.gSystem.ChangeDirectory(dirn)
    if not changedto:
        ROOT.gSystem.mkdir(dirn, True)

    ROOT.gSystem.ChangeDirectory(dirn)    
    print(".. changed to directory "+dirn)

    _save(cnv, name, dumpROOT, "")
    ROOT.gSystem.ChangeDirectory(startdir)



def save(name, dumpROOT=False):
    global _cnvs
    global _legend
    global _legendpos
    ROOT.gStyle.SetOptTitle(0)
    _cnvs[-1].Update()
    _saveToDir(_cnvs[-1], "plots", name, dumpROOT=dumpROOT)

def s(name):
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


def label(locx, locy, text, sz=0.1):
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

def mlz( h ):
    h.SetTitle("");
    h.GetYaxis().SetNdivisions(505);
    h.GetYaxis().SetTitleOffset(1.5);    h.GetXaxis().SetTitleOffset(1.2);
    h.GetYaxis().SetTitleFont(43);      h.GetYaxis().SetTitleSize(17);
    h.GetYaxis().SetLabelFont(43);      h.GetYaxis().SetLabelSize(17);
    h.GetXaxis().SetTitleFont(43);      h.GetXaxis().SetTitleSize(17);
    h.GetXaxis().SetLabelFont(43);      h.GetXaxis().SetLabelSize(17);
    h.SetLineWidth(2);

