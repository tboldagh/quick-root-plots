# quick-root-plots

This is a collection of scripts (python & bash) allowing for creation of decent quality ROOT plots (using ROOT python binding) with a minimal amount of typing.
Python version 3 is required (tested on 3.9).

```
# an example minimal script
from fast import *
h = get(_file0, "histoX")
h = get(_file0, "histoY")
cnv() # a canvas (can be skipped)
frame((10, 0, 10), (10, 0, 100)) # define axes ranges (not needed if histograms have reasonable ranges already), but often convenient to use
axis("size [mm]", "count") # label axes (not needed if original histograms have reasonably named axes)

legend("tr,uur") # legend at top right, moved even more slightly up (two quants) and right (one quant)

draw(h, "my data X")
draw(h, "my data Y") # automatically superimposed, changed symbols & colors, and added to the legend

save("comparison") # generates PDF comparisons.pdf in "plots" subdir
```
See the result of running the [testplot.py](https://github.com/tboldagh/quick-root-plots/blob/main/scripts/testplot.py).
<object data="https://github.com/tboldagh/quick-root-plots/blob/main/figures/testplot.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/tboldagh/quick-root-plots/blob/main/scripts/testplot.py">
        <p>No PDF support? <a href="https://github.com/tboldagh/quick-root-plots/blob/main/scripts/testplot.py">Download PDF</a>.</p>
    </embed>
</object>

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
Capital move directives move by 3 quants, i..e LU is the same as llluuu.
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

*Beware, there is not consistency checking among the command line and options.*
That is, it will not catch typos for you!





# Installation
Not really needed, just make the directory where the python scripts reside (i.e. fast part of you PYTHONPATH).

# TODO
* expand move directives for other elements of the plot
* a few more styles (like journal)?