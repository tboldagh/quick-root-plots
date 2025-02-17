# quick-root-plots

This is a collection of scripts (python & bash) allowing for creation of decent quality ROOT plots (using ROOT python binding) with a minimal amount of typing.
Python version 3 is required (tested on 3.9).

```
# an example minimal script
from fast import *
h = get(_file0, "histoX")
h = get(_file0, "histoY")
cnv() # a canvas
frame((10, 0, 10), (10, 0, 100)) # define axes ranges (not needed if histograms have reasonable ranges already), but often convenient to use
axis("size [mm]", "count") # label axes (not needed if original histograms have reasonably named axes)

legend("tr,uur") # legend at top right, moved even more slightly up (two quants) and right (one quant)

draw(h, "my data X")
draw(h, "my data Y") # automatically superimposed, changed symbols & colors, and added to the legend

save("comparison") # generates PDF comparisons.pdf in "plots" subdir
```
See the result of running the [testplot.py](https://github.com/tboldagh/quick-root-plots/blob/main/figures/testplot.pdf).

## What functionality is included
* getting the histograms with `get` (third argument can be used to provide a specimen histogram)
* canvas making `cnv`  with arguments can control name & sizes
* `new` to make a new plot(s) in new canvas
* `frame` to enforce the axes ranges - arguments are 3-element tuples for x and y axes, 0th number defines number of divisions: 10 is reasonable default to use, 1st and 2nd tuple element define ranges
* access to a current frame `cframe`
* `draw` function taking the histogram, label in the legend, drawing option, boolean to add or not to the legend, legend option (default is to have line and symbol). 
    Colors are decided automatically and are inspired from https://colorbrewer2.org/ for qualitative data). The symbols are as well decided. (If it needs to be customized, the `setattrs` taking `[(color, symbol)])` can be used.
* `stacks` to create stack of histograms
* `legend` to prepare the legend with a few predefined position 
* `axis` to set axes labels
* `save` to save the canvas as PDF (with dumpROOT option saves convenient ROOT file)
* `putlabel` adds text at position given by args (either explicit or via positioning key).
* `move` moves plot elements around (resizing typically do not apply). Elements that can be moved are, axes, axes labels & titles.
Pretty much all of it is used in example `testplot.py` script.

### Positioning/moving
Several functions take positioning key as an argument. They help to quickly place elements on the plot and move it a bit.
There are predefined positions for the legend:
`tr`, `tl`, `tc`, `br` where t is for top, b, bottom, r for right, c for center and l for left. So the `tl` would mean top-left.
In addition they key can be supplemented by move/resize directives that are:
* `u` move up
* `d` down
* `l` left 
* `r` right, 
* `w` widen 
* `n` to make object narrower and 
* `s` shorter
* `t` taller. 
Capital move directives move by 3 quants, i.e. LU is the same as llluuu.
# piroot 
Is a wrapper of python + ROOT that allows to execute following comamnds:
```
piroot file_with_histograms.root drawing_script.py -p "optionA=2; optionB=True"
```
The `file_with_histograms.root` is then available in the `drawing_script.py` as `_file0` (or `_files[0]`)
and `optionA` and `optionB` become variables in script global scope.
(For a more convenient delivery of options see `myop` below.)

Two more options are supported: `-a` that contains the code that is run after the script and `-q` that quits the python after drawing (else python prompt is left for you to interact with the plot).

The piroot is a bash script that generates a loading python scripts and then invokes python withe user input files & script(s).
You can always check their content by `la -a` after running at least once. 


# Options in the scripts
It is often convenient to make several plots using the same script. So you'll need option to at least pick the histogram you want to plot and decide on sth else.
The `myop` class is useful for that:
```
from myop import *
options = myop(globals())
options.hist="myDataX" # default histogram to be drawn
options.wide=False # to make the canvas very wide

print(run_args(options)) # will list options modified by the command line args
...
...
cnv("", 1000 if options.wide else 500, 500) # make use of one of the options

h = get(_file0, options.hist)

``` 

A good example of how `myop` can be use is the drawing script `draw.py`.
The definition of the options is though not limited to preamble of the drawing script. You can define the option whenever you feel need in the script.
Options in the command line can be repeated (the last set value wins) and they can be any valid python code.

An example drawing command for DATA/MC comparison:
```sh
export COMMON="legend=['DATA', 'MC']; msg=['Describe','the', 'plot'];legendpos='tl,Sl';msgsz=0.05;ratioto=1;ascale=[1, 1700/(99500./3714.)];drawopt=['root: hpe', 'root: h  fill'];"

piroot data.root mc.root draw.py -p $COMMON"hist='var_a'; yrange=(10, 0.001, 20e3); rebin=4;out='comparison_of_var_a'"

piroot data.root mc.root draw.py -p $COMMON"hist='var_b'; yrange=(10, 0.001, 1e3); logy=1;out='comparison_of_var_b'"
...
#and some more plots  
```
Some more examples of how to automate plots making can be found in scripts/examples.sh

*Beware, that there is very limited checks of command line options.*
That is, it will not catch typos for you!

# Included scripts
There is couple of "small" scripts included that are ready to be used for making quite a diverse set of plots. First of all `draw.py` can be used to draw same histogram from multiple files, multiple hitograms from one file and nearly all settings of the plot can be customised from command line. See the source code for all the options.

A simpler version, `simple.py` just good for signle histogram an only af few customizations available through command line.  

A useful script called `content.py` can be used to list content of the ROOT file like this:
``sh
piroot -q file.root content.py 
``

For interactive exploration of the ROOT file with python the `browse.py` script is provided. It repackages ROOT file as full fledged python object. An example of interactive discovery of histogram and plotting is shown below.
``sh
piroot basic_checks.root browse.py
...starting python
- - - - - - - - - - - - - - - - - - - - welcome to piROOT - opening files - - - - - - - - - - - - - - - - - - - -
.opening basic_checks.root
. indexing file content (every / is dir, every * is object )
///../../../../../.......................................................................................... done
. this is interactive browser of the ROOT file
. to browse file with tab completion start with typing: ro. and hit <TAB>
ro.<TAB> << try this
ro.basic_checks.NChR.Draw("hpe")
``




# Installation
Not really needed, just make the directory where the python scripts reside (i.e. fast part of you PYTHONPATH).

In order to use `piroot` and scripts in `scripts` subdir like `draw.py` one should
run firs: `source install_dir/quick-root-plots/scripts/thisq.sh`.




# TODO
* a few more styles (like journal)?