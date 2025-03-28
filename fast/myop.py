class myop(object):
    __scope=None
    def __init__(self, scope):
        import copy
        myop.__scope = copy.copy(scope)
        self.interactive=False

    def __repr__(self):
        return str(self.__dict__)

    def __setattr__(self, name, val):
        if name in myop.__scope:
            print ('...cmd options..',name, "=", myop.__scope[name], " default:",val)
            super(myop, self).__setattr__(name, myop.__scope[name])
            del myop.__scope[name] # clean global namespace
        else:
            super(myop, self).__setattr__(name, val)
            if hasattr(self, "help") and self.help:
                print ('...help on command line option ..',name, "default:",val)


    def run_args(self):
        args=''
        for attr in dir(self):
            if '__' in attr:
                continue
            if 'run_args' in attr:
                continue
            args += attr
            args += '='
            args += repr(self.__getattribute__(attr))
            args += ';'
        return args
    
    def save(self, filename):
        """ Save options for reuse """
        import os
        fullfname=os.environ.get("QPLOTDIR", "plots")+"/"+filename+".sh"

        with open(fullfname, "w") as f:            
            f.write('piroot ')
            f.write(' '.join([f.GetName() for f in self.__scope['_files']]))
            f.write(' '+ self.__scope['_script']+' -p ')
            f.write(' \\\n')
            f.write('"')
            f.write(
                ";".join([f'{var}={repr(value)}' for var,value in self.__dict__.items() if var != 'interactive'])
            )
            f.write('"')

        # print ('...saved used options in ', fullfname)

def run_args(options):
    return options.run_args()

if __name__ == "__main__":
    print ("""\
from myop import *
options = myop(globals())

options.etamin=0
options.etamax=1.0
print 'run with options ',  '"%s"'%  run_args(options)
    """)
