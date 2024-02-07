for f in _files:
    f.Print()

    def ldir(d, parent=""):
        for k in d.GetListOfKeys():
            print(parent+"/"+ k.GetName(), k.GetClassName() )
            if "Directory" in k.GetClassName():
                ldir(d.Get(k.GetName()), parent+"/"+k.GetName())
    ldir(f)