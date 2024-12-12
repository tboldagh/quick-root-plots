for f in _files:
    f.Print()

    def ldir(d, parent=""):
        for k in d.GetListOfKeys():
            fullname=parent.lstrip("/")+"/"+ k.GetName()
            obj = f.Get(fullname.lstrip("/"))
            print(f"{fullname:<60}", k.GetClassName(),  "Entries: "+str(obj.GetEntries()) if hasattr(obj, "GetEntries") else "")
            if "Directory" in k.GetClassName():
                ldir(d.Get(k.GetName()), fullname)
    ldir(f)