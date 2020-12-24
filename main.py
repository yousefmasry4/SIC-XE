from src.Files import File
from src.directives import Directives 
import argparse
import os
prog=None
DIRTAB = [
        "START" ,
        "END"   ,
        "BYTE"  ,
        "WORD"  ,
        "RESB"  ,
        "RESW"  ,
        "BASE"  ,
        "LTORG" ,
        "EQU" 
    ]
class Main():
    def __init__(self,fn):
        fn=File(fn)
        self.programe=fn.read(ign=[''],start_ign=[None,'.'])
        self.name = ''
        self.start_addr = None
        self.current_loc=None
        self.lineno = 0
        self.littab = {}
        self.symtab={}
        self.endlitpool = []
        self.Lines = []
        self.base = None
        self.DIR_H=Directives(self)   
    def pass1(self):
        for l in self.programe:
            self.lineno +=1
            parts=File.split_line(l)
            flag= True
            for part in parts:
                if str(part).upper() in DIRTAB:
                    flag == False
                    self.DIR_H.handel(parts,str(part).upper())
                    break
            if flag:
                pass
            exit(0)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs=1)
    args = parser.parse_args()
    print(f"compiling   {args.input[0]}")
    
    prog=Main(args.input[0])
    prog.pass1()