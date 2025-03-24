global _file0
from fast import *
class r(object):
    def __init__(self, dir, path=""):        
        self._dir = dir
        def mkpath(prefix, newpart):
            return prefix+"/"+newpart if prefix else newpart
        
        for k in list(dir.GetListOfKeys()):            
            dirname  = k.GetName().replace("-","_")
            subpath = mkpath(path, k.GetName())
            if k.GetClassName() == 'TDirectoryFile':
                print("/", end="")
                subdir = get(_file0, subpath)
                setattr(self, dirname, r(subdir, subpath))
            else:
                print(".", end="")
                setattr(self, dirname, get(_file0, subpath))

    def ls(self):
        self._dir.ls()

print(". indexing file content (every / is dir, every * is object )")
ro = r(_file0)
print(".. done ")
cnv()

print(". this is interactive browser of the ROOT file")
print(". to browse file with tab completion start with typing: ro. and hit <TAB>")

