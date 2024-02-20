


# example automation for diffing:
HIST=NONE
OPTS="out=None"
function diff(){
    piroot  MC.root DATA.root\
    draw.py -p "hist='$HIST';legend=['MC', 'DATA' ];escale=True;drawopt=['root: hpe fill', 'root hpe'];ratioto=1;out='$HIST';$OPTS"
   # can add this to scale them by an arbitraty factor (number of events/lumi) ascale=[1./8879,1./6567001.5]
}



HIST=pt OPTS="logy=1;yrange=(10, 1e-3, 1e3);xtit='p_{T} [GeV]'" # logscale, fix y range, improve x title
diff

export HIST=holes_eta_sct_ptbin9
export OPTS="yrange=(10, -0.01, 0.4);xtit='sct holes';profx=True;escale=False" # fix range, improve title, project 2D hist into x, disable scaling
diff



# example of comparing histogram from different subdirs
PL="Hist1"
COMMON="legend=['title 1', ' title 2'];ratioto=1;"
piroot INPUT.root draw.py -p $COMMON";hist=['SUB2/$PL', 'SUB1/$PL']; \
        ;xrange=(10, -5,5);xtit='#eta';yrange=(10, -0.1, 1);ytit='N_{trk}';out='effpt'"

# ...


