from src.number import Number
from src.models.Lines import Line
from src.models.literalTable import LiteralTable
from src.Files import File
from src.directives import Directives

import argparse
import os

from src.pass2 import Pass2

prog = None
DIRTAB = [
    "START",
    "END",
    "BYTE",
    "WORD",
    "RESB",
    "RESW",
    "BASE",
    "LTORG",
    "EQU",
    "RESDW"
]


class Main():
    def __init__(self, fn):
        fn = File(fn)
        self.programe = fn.read(ign=[''], start_ign=[None, '.'])
        self.name = ''
        self.start_addr = None
        self.current_loc = None
        self.lineno = 0
        self.littab = {}
        self.symtab = {}
        self.litpool = []
        self.litpoolTable = []
        self.Lines = []
        self.base = None
        self.DIR_H = Directives(self)
        self.sTypeA = []

    def pass1(self):
        #   print(self.programe)
        for l in self.programe:
            self.lineno += 1
            #   print(self.lineno)
            parts = File.split_line(l)
            flag = True
            for part in parts:

                if str(part).upper() in DIRTAB:
                    flag = False
                    self.DIR_H.handel(parts, str(part).upper())
                    break
            if flag:
                temp = Line(
                    parts,
                    self.lineno,
                    self.current_loc,
                    instr=None,
                )
                if (temp.label != None):
                    #    print(str(temp))
                    if (temp.label.upper() not in self.symtab):
                        self.symtab[temp.label.upper()] = None
                #    print(temp.label.upper(), self.symtab[temp.label.upper()])
                #    exit(0)

                self.Lines.append(temp)
                #   print(str(self.Lines[-1]))
                self.current_loc = Number(Number(self.current_loc).int() + temp.formate).hex(size=6)
                if (self.Lines[-1].label != None):
                    self.symtab[self.Lines[-1].label.upper()] = self.Lines[-1].location
            temp = self.Lines[-1]
            if temp != None:
                #    print("ssssssssssssssssssssssssssssssssssssssssssss",temp)
                if temp.pre == '=':
                    LiteralTable(self, temp.ref)
        symb = ""
        for i in self.symtab.items():
            symb += "%-6s  |" % (i[0]) + "%s|" % ("R" if i[0] not in self.sTypeA else "A") + \
                    "\t%-6s\n" % (i[1].upper()[2:])
            if (i[1] == None):
                raise Exception(f"var [{i[0]}]\tis not defined")

        if self.base is None:
            for i in self.Lines:
                if i.instruction == "LDB":
                    self.base = i.ref
        self.base = self.symtab[self.base]

        # len(self.Lines)-10  self.Lines[i].formate == 5 and not
        for i in range(0, len(self.Lines)):
            print(i)
            if not (self.Lines[i].asm):
                print("--->><<", self.Lines[i].location)
                Pass2(self.Lines, i, self.symtab, self.base)

        print("base== ", self.base)
        print(symb)
        print("**********************************************************")
        for s in self.litpoolTable:
            print(str(s))
        print("**********************************************************")
        for s in self.Lines:
            print(str(s))
        File("/media/youssef/media/SIC XE/Files/symb.txt").write(data_str=symb)
        File("/media/youssef/media/SIC XE/Files/litpoolTable.txt").write(
            data_list=[str(i) for i in self.litpoolTable])
        File("/media/youssef/media/SIC XE/Files/Lc.txt").write(data_list=[str(i) for i in self.Lines])

        "HTE RECORD"
        hte=[]
        "H"
        hte.append("H." +
              ("%-6s." % (self.name)).replace(" ", "_") +
              "%6s." % (self.start_addr[2:]) +
              str(
                  Number(
                      Number(self.current_loc[2:]).int() -
                      Number(self.start_addr).int()
                  ).hex(size=6)[2:]
              )
                   )
        "Ts"

        now = 1
        s = self.Lines[now]
        arr = []

        while True:

            def save_T(s, end):
                end = self.Lines[end]

                ans = "T.{0}.{1}.".format(
                    s.location[2:],
                    ("%2s"%Number(Number(end.location).int() - Number(s.location).int()).hex().upper()[2:]).replace(" ","0")
                )
                "array data"

                ans+=".".join(arr)
                hte.append(ans)
                print(hte)

            if now == len(self.Lines) - 1:
                print("ada")
                ans = "T.{0}.{1}.".format(
                    s.location[2:],
                    ("%2s"%str(Number(Number(self.current_loc).int() - Number(s.location).int()).hex().upper())[2:]).replace(" ","0")
                )
                "array data"

                ans+=".".join(arr)
                hte.append(ans)
                break

            if len(self.Lines[now].instruction_list) != 3 and self.Lines[now].asm == True:
                now += 1
            elif Number(self.Lines[now].location).int() - Number(s.location).int() > 29:
                print(now)
                now -= 1
                t=arr[-1]
                arr=arr[:-1]
                save_T(s, now )

                arr = []
                arr.append(t)

                s = self.Lines[now]
                now+=1
             #   exit(0)
            elif len(self.Lines[now].instruction_list) == 3 and self.Lines[now].asm == True and self.Lines[now].object_code is None:
                save_T(s, now )

                arr = []
                temp_now = now
                print(now)
                while self.Lines[temp_now].object_code is None:
                    print("       ", self.Lines[temp_now].instruction_list)
                    temp_now += 1
                now = temp_now
                s = self.Lines[now]
                print(now)
            else:
                print(self.Lines[now].instruction_list, len(self.Lines[now].instruction_list) == 3,
                      self.Lines[now].asm == True)
                arr.append(self.Lines[now].object_code)
                print(now, arr)
                now += 1

        hte.append("E.{0}".format(self.start_addr[2:]))
        print("******************************")
        for ssyy in hte:
            print("".join(ssyy) )
        File("/media/youssef/media/SIC XE/Files/HTE.txt").write(
            data_list=["".join(i)  for i in hte])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs=1)
    args = parser.parse_args()
    #   try:
    print(f"compiling   {args.input[0]}")
    prog = Main(args.input[0])
    prog.pass1()
'''
    except Exception as e:
        print(e)
'''
