from src.number import Number
from src.models.Lines import Line
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
        print(self.programe)
        for l in self.programe:
            self.lineno +=1
         #   print(self.lineno)
            parts=File.split_line(l)
            flag= True
            for part in parts:

                if str(part).upper() in DIRTAB:

                    flag = False
                    self.DIR_H.handel(parts,str(part).upper())
                    break
            if flag:
                temp=Line(
                        parts,
                        self.lineno,
                        self.current_loc,
                        instr=None,
                    )
                if(temp.label != None):
                #    print(str(temp))
                    if( temp.label.upper() not in self.symtab):
                        self.symtab[temp.label.upper()]=None
                #    print(temp.label.upper(), self.symtab[temp.label.upper()])
                #    exit(0)

                self.Lines.append(temp)
             #   print(str(self.Lines[-1]))
                self.current_loc= Number(Number(self.current_loc).int()+temp.formate).hex(size=6)
                if(self.Lines[-1].label != None ):
                    self.symtab[self.Lines[-1].label.upper()]=self.Lines[-1].location
        symb=""
        for i in self.symtab.items():
            symb +="%-6s  |"%(i[0])+"\t%-6s\n"%(i[1].upper()[2:])
            if(i[1] == None):
                raise Exception(f"var [{i[0]}]\tis not defined")
       
        print(symb)
        for s in self.Lines:
            print(str(s))
        File("/media/youssef/media/SIC XE/Files/symb.txt").write(data_str=symb)
        File("/media/youssef/media/SIC XE/Files/Lc.txt").write(data_list=[str(i) for i in self.Lines])





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs=1)
    args = parser.parse_args()
    print(f"compiling   {args.input[0]}")
    
    prog=Main(args.input[0])
    prog.pass1()
